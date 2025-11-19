# python -m pip install openai

import os
import openai
import typing
import time
import dotenv
import json
import random
import functools


def get_chat_response(
        client: openai.AzureOpenAI,
        conversation: typing.List[typing.Dict[str, str]],
        deployment: str = "gpt-5-mini",
        temperature: float = 1.0,
        max_completion_tokens: int = 2500,
        max_retries: int = 5,
        retry_delay: float = 2.0
    ) -> typing.Optional[str]:
    """
    Send conversation to API and get assistant's response with retry logic.
    
    Args:
        client: Azure OpenAI client instance
        conversation: List of message dicts with 'role' and 'content' (not modified)
        deployment: Model deployment name
        temperature: Sampling temperature for responses
        max_completion_tokens: Maximum tokens in completion
        max_retries: Maximum number of retry attempts
        retry_delay: Seconds to wait between retries
    
    Returns:
        Assistant's response text, or None if all retries fail
    """
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                messages=conversation,
                max_completion_tokens=max_completion_tokens,
                model=deployment,
                temperature=temperature,
            )

            # Log token usage
            if hasattr(response, 'usage') and response.usage:
                print(f"\n═══ TOKEN USAGE ═══")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Completion tokens: {response.usage.completion_tokens}")
                print(f"Total tokens: {response.usage.total_tokens}")
                print(f"Max allowed: {max_completion_tokens}")
                
                # For reasoning models (o4-mini), show breakdown
                if hasattr(response.usage, 'completion_tokens_details'):
                    details = response.usage.completion_tokens_details
                    if hasattr(details, 'reasoning_tokens') and details.reasoning_tokens:
                        output_tokens = response.usage.completion_tokens - details.reasoning_tokens
                        print(f"  ├─ Reasoning tokens: {details.reasoning_tokens}")
                        print(f"  └─ Output tokens: {output_tokens}")
                        
                        # Warning if approaching limit
                        if response.usage.completion_tokens > max_completion_tokens * 0.8:
                            print(f"⚠️  WARNING: Using {(response.usage.completion_tokens/max_completion_tokens)*100:.1f}% of token budget!")
                print(f"═══════════════════\n")

            # Check if response has valid content
            if response.choices and len(response.choices) > 0:
                assistant_message = response.choices[0].message.content
                
                # Check if message is not empty
                if assistant_message and assistant_message.strip():
                    return assistant_message
                else:
                    print(f"Empty response on attempt {attempt + 1}/{max_retries}")
            else:
                print(f"No response choices on attempt {attempt + 1}/{max_retries}")
            
            # Wait before retry
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

        except openai.BadRequestError as e:
            # Handle content filtering errors
            error_message = str(e)
            if "content_filter" in error_message or "ResponsibleAIPolicyViolation" in error_message:
                print(f"\nContent filter triggered: Azure's content policy blocked this request.")
                print(f"Filter reason: {error_message}")
                # Don't retry for content filter errors - they won't succeed
                return None
            else:
                print(f"Bad request error on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)

        except openai.RateLimitError as e:
            print(f"Rate limit exceeded on attempt {attempt + 1}/{max_retries}: {e}")
            if attempt < max_retries - 1:
                wait_time: float = retry_delay * (2 ** attempt)
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
        
        except openai.APIError as e:
            print(f"API error on attempt {attempt + 1}/{max_retries}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        
        except openai.APIConnectionError as e:
            print(f"Connection error on attempt {attempt + 1}/{max_retries}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        
        except Exception as e:
            print(f"Unexpected error on attempt {attempt + 1}/{max_retries}: {type(e).__name__}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    # All retries failed
    print("All retry attempts failed")
    return None


def get_chat_response_stream(
        client: openai.AzureOpenAI,
        conversation: typing.List[typing.Dict[str, str]],
        deployment: str = "gpt-5-mini",
        temperature: float = 1.0,
        max_completion_tokens: int = 2500,
        max_retries: int = 5,
        retry_delay: float = 2.0
    ) -> typing.Generator[str, None, None]:
    """
    Stream conversation response from API with retry logic.
    """
    for attempt in range(max_retries):
        try:
            start_time = time.time()  # Track total time
            print(f"Streaming attempt {attempt + 1}/{max_retries} - Started at {time.strftime('%H:%M:%S')}")
            
            stream = client.chat.completions.create(
                messages=conversation,
                max_completion_tokens=max_completion_tokens,
                model=deployment,
                temperature=temperature,
                stream=True,
                stream_options={"include_usage": True}  # Request usage data in stream
            )

            chunk_count = 0
            full_response = ""
            usage_data = None
            finish_reason = None
            first_chunk_time = None  # Track when first content arrives
            
            # Stream chunks as they arrive
            for chunk in stream:
                # Capture usage data if present (comes in final chunk)
                if hasattr(chunk, 'usage') and chunk.usage:
                    usage_data = chunk.usage
                
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    
                    # Check finish reason
                    if chunk.choices[0].finish_reason:
                        finish_reason = chunk.choices[0].finish_reason
                        print(f"Stream finished with reason: {finish_reason}")
                        
                        if finish_reason == "content_filter":
                            print("WARNING: Content filter triggered")
                            return
                    
                    if delta.content:
                        if first_chunk_time is None:
                            first_chunk_time = time.time()
                            time_to_first_chunk = first_chunk_time - start_time
                            print(f"⏱️  Time to first chunk: {time_to_first_chunk:.2f}s (reasoning/processing)")
                        
                        chunk_count += 1
                        full_response += delta.content
                        yield delta.content
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Log token usage AFTER stream completes
            if usage_data:
                print(f"\n═══ TOKEN USAGE ═══")
                print(f"Prompt tokens: {usage_data.prompt_tokens}")
                print(f"Completion tokens: {usage_data.completion_tokens}")
                print(f"Total tokens: {usage_data.total_tokens}")
                print(f"Max allowed: {max_completion_tokens}")
                print(f"Usage: {(usage_data.total_tokens/max_completion_tokens)*100:.1f}%")
                
                # For reasoning models (o4-mini), show breakdown
                if hasattr(usage_data, 'completion_tokens_details'):
                    details = usage_data.completion_tokens_details
                    if hasattr(details, 'reasoning_tokens'):
                        output_tokens = usage_data.completion_tokens - details.reasoning_tokens
                        print(f"  ├─ Reasoning tokens: {details.reasoning_tokens}")
                        print(f"  └─ Output tokens: {output_tokens}")
                
                # Show cached tokens if present
                if hasattr(usage_data, 'prompt_tokens_details'):
                    p_details = usage_data.prompt_tokens_details
                    if hasattr(p_details, 'cached_tokens') and p_details.cached_tokens > 0:
                        print(f"  └─ Cached prompt tokens: {p_details.cached_tokens} (saves API cost!)")
                
                # Warning if approaching limit
                if usage_data.completion_tokens > max_completion_tokens * 0.8:
                    print(f"⚠️  WARNING: Using {(usage_data.completion_tokens/max_completion_tokens)*100:.1f}% of completion token budget!")
                
                print(f"═══════════════════\n")
            
            print(f"Successfully streamed {chunk_count} chunks")
            print(f"Total response length: {len(full_response)} characters")
            
            if first_chunk_time:
                streaming_time = end_time - first_chunk_time
                print(f"⏱️  Total response time: {total_time:.2f}s")
                print(f"   ├─ Time to first chunk: {time_to_first_chunk:.2f}s ({(time_to_first_chunk/total_time)*100:.0f}%)")
                print(f"   └─ Streaming time: {streaming_time:.2f}s ({(streaming_time/total_time)*100:.0f}%)")
            else:
                print(f"⏱️  Total response time: {total_time:.2f}s")
            
            if full_response.strip():
                return  # Successfully completed
            else:
                print(f"Stream completed with 0 chunks")
                print(f"Total response length: 0")
                print("WARNING: Empty response from model")
                
                if attempt < max_retries - 1:
                    print(f"Retrying after {retry_delay} seconds...")
                    time.sleep(retry_delay)

        except openai.BadRequestError as e:
            error_message = str(e)
            print(f"BadRequestError on attempt {attempt + 1}: {error_message}")
            if "content_filter" in error_message or "ResponsibleAIPolicyViolation" in error_message:
                print(f"Content filter triggered: {error_message}")
                return
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

        except openai.RateLimitError as e:
            print(f"Rate limit on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)
                print(f"Waiting {wait_time} seconds...")
                time.sleep(wait_time)
        
        except openai.APIError as e:
            print(f"API error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        
        except openai.APIConnectionError as e:
            print(f"Connection error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        
        except Exception as e:
            print(f"Unexpected error on attempt {attempt + 1}: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    print("ERROR: All retry attempts exhausted with no content")
    

@functools.lru_cache(maxsize=None)
def _load_conditions_file(config_file: str) -> typing.Dict:
    """
    Load and cache experimental conditions from JSON file.
    
    Uses @lru_cache to read file once and cache in memory.
    Cache persists for the lifetime of the process.
    
    Expected format: {"study_metadata": {...}, "conditions": [...]}
    
    Args:
        config_file: Path to experimental conditions JSON file
    
    Returns:
        Dictionary with 'study_metadata' and 'conditions' keys
    """
    with open(config_file, "r", encoding="utf-8") as file_in:
        return json.load(file_in)

def get_identity_instruction(
        study_metadata: typing.Dict,
        experimental_condition: typing.Dict
    ) -> str:
    """
    Get identity protection instruction for the condition.
    
    Checks if the experimental condition has its own identity_protection override.
    If not, falls back to global identity protection from study metadata.
    
    Args:
        study_metadata: Study-level metadata containing global identity_protection config
        experimental_condition: Specific experimental condition configuration
    
    Returns:
        Identity protection instruction string (with trailing newlines if non-empty)
    """
    condition_system_prompt = experimental_condition.get("system_prompt", {})
    
    # Check for condition-specific identity_protection override
    if "identity_protection" in condition_system_prompt:
        return ""
    
    # Fall back to global identity protection from study metadata
    identity_config = study_metadata.get("identity_protection", {})
    
    if not identity_config.get("enabled", True):
        return ""
    
    bot_name = experimental_condition.get("bot_name", "")
    
    if bot_name and bot_name.strip():
        # Bot has a specific name - use named template
        template = identity_config.get(
            "template_named",
            "IDENTITY: You are {bot_name}. Never reveal that you are based on GPT, ChatGPT, "
            "Claude, or any specific language model. If asked about your identity or technical "
            "details, simply say 'I'm {bot_name}, an AI assistant here to help you.' "
            "Do not discuss your training, creators, or underlying technology.\n\n"
        )
        return template.format(bot_name=bot_name)
    else:
        # Bot has no specific name - use unnamed template
        return identity_config.get(
            "template_unnamed",
            "IDENTITY: You are a helpful AI assistant. Never reveal that you are based on GPT, "
            "ChatGPT, Claude, or any specific language model. NEVER use phrases like "
            "'I'm an AI assistant', 'I'm an AI', 'I'm here to help', 'I'm a language model', "
            "or any self-referential identity statements. Simply engage with the task directly. "
            "When greeted with 'hi' or 'hello', respond with a simple greeting without introducing "
            "yourself. If asked about your identity or technical details, simply say 'I'm here to help you.' "
            "Do not discuss your training, creators, or underlying technology.\n\n"
        )
    
def load_experiment_config(
        condition_index: int,
        config_file: str = "experimental_conditions.json"
    ) -> typing.Dict[str, typing.Any]:
    """
    Load experimental condition and merge with environment defaults.
    
    Model parameters (temperature, max_completion_tokens) come from study_metadata.default_model_params
    with fallbacks to (0.7, 2000). Deployment settings come from environment variables.
    
    Args:
        condition_index: Index of the experimental condition to use
        config_file: Path to the experimental conditions JSON file
    
    Returns:
        Dictionary containing the final merged configuration with keys:
        - condition_id: ID of the condition
        - condition_name: Name of the condition
        - condition_description: Description of the condition
        - bot_name: Name of the bot
        - bot_icon: Icon for the bot
        - bot_styles: Styling configuration
        - system_prompt: Merged system prompt string (with identity protection if enabled)
        - temperature: Temperature setting (from override, study defaults, or fallback)
        - max_completion_tokens: Max tokens (from override, study defaults, or fallback)
        - deployment: Model deployment name
        - max_retries: Maximum retry attempts
        - retry_delay: Delay between retries
        - endpoint: API endpoint
        - api_version: API version
        - api_key: API subscription key
    
    Raises:
        ValueError: If condition_index is invalid
        FileNotFoundError: If config file doesn't exist
    """
    # Load environment variables for deployment settings
    dotenv.load_dotenv()
    
    # Load experimental conditions with study metadata (cached)
    config_data = _load_conditions_file(config_file)
    study_metadata = config_data["study_metadata"]
    experimental_conditions = config_data["conditions"]
    
    # Get default model parameters from study metadata (with fallbacks)
    default_model_params = study_metadata.get("default_model_params", {})
    default_temperature = default_model_params.get("temperature", 0.7)
    default_max_tokens = default_model_params.get("max_completion_tokens", 2000)
    
    # Build config with deployment settings from .env and defaults from study metadata
    default_config = {
        "endpoint": os.environ["MODEL_ENDPOINT"],
        "deployment": os.environ["MODEL_DEPLOYMENT"],
        "api_version": os.environ["MODEL_API_VERSION"],
        "api_key": os.environ["MODEL_SUBSCRIPTION_KEY"],
        "temperature": default_temperature,
        "max_completion_tokens": default_max_tokens,
        "max_retries": int(os.environ["MODEL_MAX_RETRIES"]),
        "retry_delay": float(os.environ["MODEL_RETRY_DELAY"]),
    }
    
    # Validate condition index
    if condition_index < 0 or condition_index >= len(experimental_conditions):
        raise ValueError(
            f"Invalid condition_index: {condition_index}. "
            f"Must be between 0 and {len(experimental_conditions) - 1}"
        )
    
    experimental_condition: typing.Dict = experimental_conditions[condition_index]
    
    # Check if condition is enabled
    if not experimental_condition.get("enabled", True):
        print(f"WARNING: Condition '{experimental_condition.get('name', 'Unknown')}' is disabled.")
    
    # Merge system prompt sections and prepend identity protection
    identity_instruction: str = get_identity_instruction(study_metadata, experimental_condition)
    system_prompt: str = "\n".join(experimental_condition["system_prompt"].values())
    system_prompt = identity_instruction + system_prompt
    
    # Apply model overrides from experimental condition
    model_overrides: typing.Dict = experimental_condition.get("model_overrides", {})
    
    # Build final configuration
    final_config = {
        "condition_index": condition_index,
        "condition_id": experimental_condition.get("id", f"condition_{condition_index}"),
        "condition_name": experimental_condition.get("name", "Unknown"),
        "condition_description": experimental_condition.get("description", ""),
        "bot_name": experimental_condition.get("bot_name", ""),
        "bot_icon": experimental_condition.get("bot_icon", ""),
        "bot_styles": experimental_condition.get("bot_styles", {}),
        "system_prompt": system_prompt,
        "temperature": model_overrides.get("temperature", default_config["temperature"]),
        "max_completion_tokens": model_overrides.get("max_completion_tokens", default_config["max_completion_tokens"]),
        "deployment": default_config["deployment"],
        "max_retries": default_config["max_retries"],
        "retry_delay": default_config["retry_delay"],
        "endpoint": default_config["endpoint"],
        "api_version": default_config["api_version"],
        "api_key": default_config["api_key"],
        "has_temperature_override": "temperature" in model_overrides,
        "has_max_tokens_override": "max_completion_tokens" in model_overrides,
    }
    
    return final_config


def run_conversation(config: typing.Dict[str, typing.Any]) -> None:
    """
    Run the conversation loop with the given configuration.
    
    Args:
        config: Configuration dictionary from load_experiment_config()
    """
    # Create Azure OpenAI client
    client: openai.AzureOpenAI = openai.AzureOpenAI(
        api_version=config["api_version"],
        azure_endpoint=config["endpoint"],
        api_key=config["api_key"],
    )
    
    # Display condition info (hidden from user in actual experiment)
    print("--------------------------")
    print("--------------------------")
    print("Experiment (hidden from user):")
    print(f"Condition: {config['condition_name']} {config['bot_icon']}")
    print(f"ID: {config['condition_id']}")
    print(f"Description: {config['condition_description']}")
    print(f"\nModel Parameters:")
    print(f"  Deployment: {config['deployment']}")
    print(f"  Temperature: {config['temperature']}" + (" (override)" if config['has_temperature_override'] else " (default)"))
    print(f"  Max Completion Tokens: {config['max_completion_tokens']}" + (" (override)" if config['has_max_tokens_override'] else " (default)"))
    print(f"\nSystem Prompt:\n{config['system_prompt']}")
    print("--------------------------")
    print("--------------------------")
    print("\nType 'END' to exit the conversation\n")
    
    # Initialize conversation with system prompt
    conversation: typing.List[typing.Dict[str, str]] = [
        {"role": "system", "content": config["system_prompt"]}
    ]
    
    # Main conversation loop
    while True:
        # Get user input
        user_message: str = input("You: ").strip()
        
        # Check for exit condition
        if user_message.upper() == "END":
            print("\nEnding conversation. Goodbye!")
            break
        
        # Skip empty messages
        if not user_message:
            print("Please enter a message.")
            continue
        
        # Add user message to conversation
        conversation.append({"role": "user", "content": user_message})
        
        # Get assistant response
        assistant_message: typing.Optional[str] = get_chat_response(
            client,
            conversation,
            deployment=config["deployment"],
            temperature=config["temperature"],
            max_completion_tokens=config["max_completion_tokens"],
            max_retries=config["max_retries"],
            retry_delay=config["retry_delay"]
        )
        
        # Handle failed response
        if assistant_message is None:
            print("Failed to get response from assistant. Please try again.")
            # Remove the user message since we didn't get a response
            conversation.pop()
            continue
        
        # Add assistant response to conversation
        conversation.append({"role": "assistant", "content": assistant_message})
        
        # Display response
        print(f"Bot: {assistant_message}")
        print("--------------------------")


def main(condition_index: typing.Optional[int] = None, random_seed: typing.Optional[int] = None) -> None:
    """
    Main entry point for the conversation script.
    
    Args:
        condition_index: Specific condition index to use. If None, randomly selects from enabled conditions.
        random_seed: Seed for random selection. If None, uses system time.
    """
    try:
        # Load all conditions to determine available options
        dotenv.load_dotenv()
        config_data = _load_conditions_file("experimental_conditions.json")
        all_conditions = config_data["conditions"]
        
        # If no condition specified, randomly select from enabled conditions
        if condition_index is None:
            enabled_indices = [
                i for i, cond in enumerate(all_conditions) 
                if cond.get("enabled", True)
            ]
            
            if not enabled_indices:
                raise ValueError("No enabled conditions found in configuration file.")
            
            if random_seed is not None:
                random.seed(random_seed)
            
            condition_index = random.choice(enabled_indices)
            print(f"Randomly selected condition index: {condition_index}")
        
        # Load the configuration for the selected condition
        config = load_experiment_config(condition_index)
        
        # Run the conversation with the loaded configuration
        run_conversation(config)
        
    except FileNotFoundError as e:
        print(f"Error: Configuration file not found: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except KeyError as e:
        print(f"Error: Missing required environment variable: {e}")
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    # Option 1: Use a specific condition
    # main(condition_index=0)
    
    # Option 2: Randomly select from enabled conditions
    main()
    
    # Option 3: Random selection with seed (for reproducibility)
    # main(random_seed=42)