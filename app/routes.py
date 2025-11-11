"""
Routes and view functions for the chat application.
"""

import typing
import re
import secrets

from flask import Blueprint, render_template, request, jsonify, Response, stream_with_context
from sqlalchemy.exc import IntegrityError

from app import db, get_azure_client, limiter
from app.models import Participant, Message
from bot import get_chat_response, load_experiment_config

main_bp = Blueprint('main', __name__)

# Constants for validation
VALID_CONDITION_RANGE = (0, 8)  # Valid condition indices: 0-8 inclusive
MAX_MESSAGE_LENGTH = 2000        # Maximum characters per message (~500 tokens)


def validate_participant_id(participant_id: str) -> bool:
    """
    Validate participant ID format.
    
    Accepts:
    - Alphanumeric characters (A-Z, a-z, 0-9)
    - Hyphens (-)
    - Underscores (_)
    - Length: 1-255 characters
    
    Rejects:
    - Special characters
    - Path traversal attempts
    - Whitespace-only IDs
    - Empty strings
    - Too long IDs
    
    Args:
        participant_id: The participant ID to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not participant_id or not participant_id.strip():
        return False
    
    # Allow alphanumeric, hyphens, underscores only, 1-255 characters
    # Hyphen at start of character class to avoid range interpretation
    return bool(re.match(r'^[-a-zA-Z0-9_]{1,255}$', participant_id))


def validate_condition_index(condition_index: typing.Optional[int]) -> bool:
    """
    Validate condition index is within valid range.
    
    Args:
        condition_index: The condition index to validate
    
    Returns:
        True if valid, False otherwise
    """
    if condition_index is None:
        return False
    
    min_condition, max_condition = VALID_CONDITION_RANGE
    return min_condition <= condition_index <= max_condition


def get_or_create_participant(participant_id: str, condition_index: int, config: typing.Dict[str, typing.Any]) -> Participant:
    """
    Get existing participant or create new one.
    Thread-safe with retry logic to handle race conditions.
    """
   
    # Try to get existing participant first
    participant = Participant.query.get(participant_id)
    if participant is not None:
        return participant
    
    # Participant doesn't exist - try to create
    # Use retry logic to handle race condition where two requests
    # try to create the same participant simultaneously
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            # Generate cryptographically secure random token
            session_token = secrets.token_urlsafe(32)
            
            participant = Participant(
                participant_id=participant_id,
                session_token=session_token,
                condition_index=condition_index,
                condition_id=config['condition_id'],
                condition_name=config['condition_name']
            )
            db.session.add(participant)
            
            system_message = Message(
                participant_id=participant_id,
                role='system',
                content=config['system_prompt']
            )
            db.session.add(system_message)
            
            db.session.commit()
            
            # Successfully created
            return participant
            
        except IntegrityError as e:
            # Another request created this participant first
            db.session.rollback()
            print(f"Race condition on participant creation (attempt {attempt + 1}/{max_attempts}): {e}")
            
            # Query again - the other request should have created it
            participant = Participant.query.get(participant_id)
            if participant is not None:
                return participant
            
            # If still None and not last attempt, try again
            if attempt < max_attempts - 1:
                import time
                time.sleep(0.1)  # Brief delay before retry
    
    # Should never get here, but handle gracefully
    raise RuntimeError(f"Failed to get or create participant {participant_id} after {max_attempts} attempts")


def get_conversation_history(participant_id: str) -> typing.List[typing.Dict[str, str]]:
    """Retrieve conversation history for a participant."""
    messages = Message.query.filter_by(participant_id=participant_id).order_by(Message.timestamp).all()
    return [{"role": msg.role, "content": msg.content} for msg in messages]


# ============================================================================
# Health Check Endpoints
# ============================================================================

@main_bp.route('/health')
def health():
    """Health check endpoint for Docker and Kubernetes."""
    return jsonify({'status': 'healthy'}), 200


@main_bp.route('/ready')
def ready():
    """Readiness check endpoint."""
    try:
        # Check database connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify({'status': 'ready'}), 200
    except Exception as e:
        return jsonify({'status': 'not ready', 'error': str(e)}), 503


# ============================================================================
# Application Routes
# ============================================================================

@main_bp.route('/')
def index():
    """Main test page with demo controls."""
    return render_template('test_interface.html')


@main_bp.route('/gui')
def chat_interface():
    """Chat interface - expects participant_id and condition as URL params."""
    participant_id = request.args.get('participant_id')
    condition_index = request.args.get('condition', type=int)
    task_active = request.args.get('task_active', default='true').lower() != 'false'
    
    # Validate participant_id
    if not participant_id:
        return jsonify({'error': 'participant_id parameter is required'}), 400
    
    if not validate_participant_id(participant_id):
        return jsonify({
            'error': 'Invalid participant_id format. Use letters, numbers, hyphens, and underscores only (max 255 characters).'
        }), 400
    
    # Validate condition_index
    if condition_index is None:
        return jsonify({'error': 'condition parameter is required'}), 400
    
    if not validate_condition_index(condition_index):
        min_cond, max_cond = VALID_CONDITION_RANGE
        return jsonify({
            'error': f'Invalid condition. Must be between {min_cond} and {max_cond}.'
        }), 400
    
    try:
        # Load config once
        config = load_experiment_config(condition_index)
        
        # Pass config to participant creation
        participant = get_or_create_participant(participant_id, condition_index, config)
        
        # Log task state change if inactive (for PI review)
        if not task_active:
            # Check if we need to log this state change
            last_message = Message.query.filter_by(
                participant_id=participant_id
            ).order_by(Message.timestamp.desc()).first()
            
            # Only log if the last message wasn't already a task_inactive marker
            if not last_message or 'TASK_STATE: inactive' not in last_message.content:
                state_marker = Message(
                    participant_id=participant_id,
                    role='system',
                    content='TASK_STATE: inactive - Task completion mode enabled'
                )
                db.session.add(state_marker)
                db.session.commit()
        
        return render_template('chat.html', 
                             participant_id=participant_id,
                             session_token=participant.session_token,
                             task_active=task_active,
                             config=config)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_bp.route('/api/send_message', methods=['POST'])
@limiter.limit("30 per minute")  # Prevent spam/abuse
@limiter.limit("500 per day")     # Daily cap for safety
def send_message():
    """Handle incoming user messages and return assistant response."""
    try:
        data = request.get_json()
        participant_id = data.get('participant_id')
        session_token = data.get('session_token')
        condition_index = data.get('condition_index')
        user_message = data.get('message', '').strip()
        
        # Validate participant_id
        if not participant_id:
            return jsonify({'error': 'participant_id is required'}), 400
        
        if not validate_participant_id(participant_id):
            return jsonify({
                'error': 'Invalid participant_id format. Use letters, numbers, hyphens, and underscores only.'
            }), 400
        
        # Validate session_token
        if not session_token:
            return jsonify({'error': 'session_token is required'}), 400
        
        # Authenticate: Verify session token matches participant
        participant = Participant.query.get(participant_id)
        if not participant or participant.session_token != session_token:
            return jsonify({'error': 'Invalid session token'}), 403
        
        # Validate condition_index
        if condition_index is None:
            return jsonify({'error': 'condition_index is required'}), 400
        
        if not validate_condition_index(condition_index):
            min_cond, max_cond = VALID_CONDITION_RANGE
            return jsonify({
                'error': f'Invalid condition_index. Must be between {min_cond} and {max_cond}.'
            }), 400
        
        # Validate message
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Check message length to prevent abuse and excessive costs
        if len(user_message) > MAX_MESSAGE_LENGTH:
            return jsonify({
                'error': f'Message too long. Maximum {MAX_MESSAGE_LENGTH} characters allowed.'
            }), 400
        
        config = load_experiment_config(condition_index)
        
        # Save user message immediately for research purposes
        # (preserves what user typed even if LLM fails to respond)
        new_user_msg = Message(
            participant_id=participant_id,
            role='user',
            content=user_message
        )
        db.session.add(new_user_msg)
        db.session.commit()
        
        # Get task_active flag (defaults to True for backward compatibility)
        task_active = data.get('task_active', True)
        
        conversation = get_conversation_history(participant_id)
        
        # Handle task_active override
        if not task_active:
            # Task is inactive - inject override to prevent task work
            task_complete_override = {
                "role": "system",
                "content": (
                    "CRITICAL OVERRIDE: The main task is now complete. "
                    "You must politely decline any requests to continue or restart the task. "
                    "Suggested responses:\n"
                    "- 'That activity is complete.'\n"
                    "- 'I've finished helping with that. Feel free to continue with the survey!'\n"
                    "You may still have friendly conversations about other topics."
                )
            }
            conversation.insert(1, task_complete_override)
        else:
            # Task is active - remove any previous override messages
            conversation = [
                msg for msg in conversation 
                if not (msg.get('role') == 'system' and 'CRITICAL OVERRIDE' in msg.get('content', ''))
            ]
        
        client = get_azure_client()
        assistant_message = get_chat_response(
            client,
            conversation,
            deployment=config["deployment"],
            temperature=config["temperature"],
            max_completion_tokens=config["max_completion_tokens"],
            max_retries=config["max_retries"],
            retry_delay=config["retry_delay"]
        )
        
        if assistant_message is None:
            # Keep user message in database for research analysis
            # This helps track what participants were trying when system failed
            return jsonify({'error': 'Failed to get response from assistant'}), 500
        
        new_assistant_msg = Message(
            participant_id=participant_id,
            role='assistant',
            content=assistant_message
        )
        db.session.add(new_assistant_msg)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': assistant_message,
            'timestamp': new_assistant_msg.timestamp.isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_bp.route('/api/send_message_stream', methods=['POST'])
@limiter.limit("30 per minute")
@limiter.limit("500 per day")
def send_message_stream():
    """Handle incoming user messages and stream assistant response."""
    from bot import get_chat_response_stream
    
    try:
        data = request.get_json()
        participant_id = data.get('participant_id')
        session_token = data.get('session_token')
        condition_index = data.get('condition_index')
        user_message = data.get('message', '').strip()
        
        # Validate participant_id
        if not participant_id:
            return jsonify({'error': 'participant_id is required'}), 400
        
        if not validate_participant_id(participant_id):
            return jsonify({
                'error': 'Invalid participant_id format.'
            }), 400
        
        # Validate session_token
        if not session_token:
            return jsonify({'error': 'session_token is required'}), 400
        
        # Authenticate
        participant = Participant.query.get(participant_id)
        if not participant or participant.session_token != session_token:
            return jsonify({'error': 'Invalid session token'}), 403
        
        # Validate condition_index
        if condition_index is None:
            return jsonify({'error': 'condition_index is required'}), 400
        
        if not validate_condition_index(condition_index):
            min_cond, max_cond = VALID_CONDITION_RANGE
            return jsonify({
                'error': f'Invalid condition_index. Must be between {min_cond} and {max_cond}.'
            }), 400
        
        # Validate message
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        if len(user_message) > MAX_MESSAGE_LENGTH:
            return jsonify({
                'error': f'Message too long. Maximum {MAX_MESSAGE_LENGTH} characters allowed.'
            }), 400
        
        config = load_experiment_config(condition_index)
        
        # Save user message
        new_user_msg = Message(
            participant_id=participant_id,
            role='user',
            content=user_message
        )
        db.session.add(new_user_msg)
        db.session.commit()
        
        # Get task_active flag (defaults to True for backward compatibility)
        task_active = data.get('task_active', True)
        
        conversation = get_conversation_history(participant_id)
        
        # Handle task_active override
        if not task_active:
            # Task is inactive - inject override to prevent task work
            task_complete_override = {
                "role": "system",
                "content": (
                    "CRITICAL OVERRIDE: The main task is now complete. "
                    "You must politely decline any requests to continue or restart the task. "
                    "Suggested responses:\n"
                    "- 'That activity is complete.'\n"
                    "- 'I've finished helping with that. Feel free to continue with the survey!'\n"
                    "You may still have friendly conversations about other topics."
                )
            }
            conversation.insert(1, task_complete_override)
        else:
            # Task is active - remove any previous override messages
            conversation = [
                msg for msg in conversation 
                if not (msg.get('role') == 'system' and 'CRITICAL OVERRIDE' in msg.get('content', ''))
            ]

        def generate():
            """Generator function for streaming response."""
            client = get_azure_client()
            full_response = []
            
            try:
                chunk_count = 0
                for chunk in get_chat_response_stream(
                    client,
                    conversation,
                    deployment=config["deployment"],
                    temperature=config["temperature"],
                    max_completion_tokens=config["max_completion_tokens"],
                    max_retries=config["max_retries"],
                    retry_delay=config["retry_delay"]
                ):
                    chunk_count += 1
                    full_response.append(chunk)
                    
                    # Encode newlines as placeholder
                    encoded_chunk = chunk.replace('\n', '<NEWLINE>')
                    yield f"data: {encoded_chunk}\n\n"
                
                print(f"Stream completed with {chunk_count} chunks")
                
                # Save complete response to database
                assistant_message = ''.join(full_response)
                print(f"Total response length: {len(assistant_message)}")
                
                if assistant_message:
                    new_assistant_msg = Message(
                        participant_id=participant_id,
                        role='assistant',
                        content=assistant_message
                    )
                    db.session.add(new_assistant_msg)
                    db.session.commit()
                    
                    yield "data: [DONE]\n\n"
                else:
                    print("WARNING: Empty response from model")
                    yield "data: [ERROR]\n\n"
            
            except Exception as e:
                print(f"Stream error: {e}")
                import traceback
                traceback.print_exc()
                yield "data: [ERROR]\n\n"

        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
            }
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_bp.route('/api/get_history', methods=['GET'])
def get_history():
    """Retrieve conversation history for current participant."""
    try:
        participant_id = request.args.get('participant_id')
        session_token = request.args.get('session_token')
        
        if not participant_id:
            return jsonify({'error': 'participant_id is required'}), 400
        
        if not validate_participant_id(participant_id):
            return jsonify({
                'error': 'Invalid participant_id format. Use letters, numbers, hyphens, and underscores only.'
            }), 400
        
        # Validate session_token
        if not session_token:
            return jsonify({'error': 'session_token is required'}), 400
        
        # Authenticate: Verify session token matches participant
        participant = Participant.query.get(participant_id)
        if not participant or participant.session_token != session_token:
            return jsonify({'error': 'Invalid session token'}), 403
        
        messages = Message.query.filter_by(participant_id=participant_id).order_by(Message.timestamp).all()
        display_messages = [msg.to_dict() for msg in messages if msg.role != 'system']
        
        return jsonify({
            'success': True,
            'messages': display_messages
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500