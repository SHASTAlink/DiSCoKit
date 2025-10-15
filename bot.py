# python -m pip install openai

import os
import openai
import typing
import time
import dotenv
import json
import random
from functools import lru_cache


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

            """
            if hasattr(response, 'usage'):
                print(f"Token usage - Prompt: {response.usage.prompt_tokens}, "
                      f"Completion: {response.usage.completion_tokens}, "
                      f"Total: {response.usage.total_tokens}")
            """

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


@lru_cache(maxsize=None)
def _load_conditions_file(config_file: str) -> typing.List[typing.Dict]:
    """
    Load and cache experimental conditions from JSON file.
    
    Uses @lru_cache to read file once and cache in memory.
    Cache persists for the lifetime of the process.
    
    Args:
        config_file: Path to experimental conditions JSON file
    
    Returns:
        List of condition dictionaries
    """
    with open(config_file, "r", encoding="utf-8") as file_in:
        return json.load(file_in)


def load_experiment_config(
        condition_index: int,
        config_file: str = "experimental_conditions.json"
    ) -> typing.Dict[str, typing.Any]:
    """
    Load experimental condition and merge with environment defaults.
    
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
        - system_prompt: Merged system prompt string
        - temperature: Temperature setting (from override or default)
        - max_completion_tokens: Max tokens (from override or default)
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
    # Load environment variables as defaults
    dotenv.load_dotenv()
    
    default_config = {
        "endpoint": os.environ["MODEL_ENDPOINT"],
        "deployment": os.environ["MODEL_DEPLOYMENT"],
        "api_version": os.environ["MODEL_API_VERSION"],
        "api_key": os.environ["MODEL_SUBSCRIPTION_KEY"],
        "temperature": float(os.environ["MODEL_TEMPERATURE"]),
        "max_completion_tokens": int(os.environ["MODEL_MAX_COMPLETION_TOKENS"]),
        "max_retries": int(os.environ["MODEL_MAX_RETRIES"]),
        "retry_delay": float(os.environ["MODEL_RETRY_DELAY"]),
    }
    
    # Load experimental conditions (cached)
    experimental_conditions = _load_conditions_file(config_file)
    
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
    
    # Merge system prompt sections
    system_prompt: str = "\n".join(experimental_condition["system_prompt"].values())
    
    # Apply model overrides from experimental condition
    model_overrides: typing.Dict = experimental_condition.get("model_overrides", {})
    
    # Build final configuration
    final_config = {
        "condition_index": condition_index,
        "condition_id": experimental_condition.get("id", f"condition_{condition_index}"),
        "condition_name": experimental_condition.get("name", "Unknown"),
        "condition_description": experimental_condition.get("description", ""),
        "bot_name": experimental_condition.get("bot_name", "Assistant"),
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
        all_conditions = _load_conditions_file("experimental_conditions.json")
        
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