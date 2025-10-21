"""
Database utilities for managing experimental chat data.
Provides tools for exporting, analyzing, and managing the conversation database.
"""

import json
import csv
import argparse
from datetime import datetime
from collections import defaultdict
from app import create_app, db
from app.models import Participant, Message


def export_to_json(output_file='data/export_data.json'):
    """Export all data to JSON format."""
    app = create_app()
    with app.app_context():
        participants = Participant.query.all()
        
        export_data = {
            'export_timestamp': datetime.utcnow().isoformat(),
            'total_participants': len(participants),
            'participants': []
        }
        
        for participant in participants:
            messages = Message.query.filter_by(
                participant_id=participant.participant_id
            ).order_by(Message.timestamp).all()
            
            participant_data = {
                'participant_id': participant.participant_id,
                'condition_index': participant.condition_index,
                'condition_id': participant.condition_id,
                'condition_name': participant.condition_name,
                'created_at': participant.created_at.isoformat(),
                'updated_at': participant.updated_at.isoformat(),
                'total_messages': len(messages),
                'user_messages': sum(1 for m in messages if m.role == 'user'),
                'assistant_messages': sum(1 for m in messages if m.role == 'assistant'),
                'conversation': [
                    {
                        'role': msg.role,
                        'content': msg.content,
                        'timestamp': msg.timestamp.isoformat()
                    }
                    for msg in messages
                ]
            }
            
            export_data['participants'].append(participant_data)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(participants)} participants to {output_file}")
        return export_data


def export_to_csv(output_file='data/export_messages.csv'):
    """Export all messages to CSV format (one row per message)."""
    app = create_app()
    with app.app_context():
        messages = Message.query.order_by(Message.participant_id, Message.timestamp).all()
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'message_id', 'participant_id', 'condition_index', 
                'condition_id', 'condition_name', 'role', 
                'content', 'timestamp'
            ])
            
            for msg in messages:
                participant = Participant.query.get(msg.participant_id)
                writer.writerow([
                    msg.id,
                    msg.participant_id,
                    participant.condition_index if participant else None,
                    participant.condition_id if participant else None,
                    participant.condition_name if participant else None,
                    msg.role,
                    msg.content,
                    msg.timestamp.isoformat()
                ])
        
        print(f"✅ Exported {len(messages)} messages to {output_file}")


def export_conversations_csv(output_file='data/conversations.csv'):
    """
    Export conversations to CSV format (one row per participant).
    Each row contains: participant_id, condition, full_conversation
    """
    app = create_app()
    with app.app_context():
        participants = Participant.query.order_by(Participant.created_at).all()
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'participant_id', 
                'condition_index', 
                'condition_id',
                'condition_name',
                'message_count',
                'full_conversation',
                'created_at',
                'updated_at'
            ])
            
            for participant in participants:
                messages = Message.query.filter_by(
                    participant_id=participant.participant_id
                ).order_by(Message.timestamp).all()
                
                # Format conversation as text (excluding system messages)
                conversation_lines = []
                for msg in messages:
                    if msg.role == 'user':
                        conversation_lines.append(f"User: {msg.content}")
                    elif msg.role == 'assistant':
                        conversation_lines.append(f"Assistant: {msg.content}")
                
                full_conversation = "\n\n".join(conversation_lines)
                message_count = len([m for m in messages if m.role != 'system'])
                
                writer.writerow([
                    participant.participant_id,
                    participant.condition_index,
                    participant.condition_id,
                    participant.condition_name,
                    message_count,
                    full_conversation,
                    participant.created_at.isoformat(),
                    participant.updated_at.isoformat()
                ])
        
        print(f"✅ Exported {len(participants)} participant conversations to {output_file}")



def get_statistics():
    """Print statistics about the collected data."""
    app = create_app()
    with app.app_context():
        participants = Participant.query.all()
        messages = Message.query.all()
        
        # Basic stats
        print("\n" + "="*60)
        print("DATABASE STATISTICS")
        print("="*60)
        print(f"\nTotal Participants: {len(participants)}")
        print(f"Total Messages: {len(messages)}")
        
        # By condition
        by_condition = defaultdict(int)
        for p in participants:
            by_condition[p.condition_name] += 1
        
        print("\nParticipants by Condition:")
        for condition, count in sorted(by_condition.items()):
            print(f"  {condition}: {count}")
        
        # Message counts
        user_msgs = sum(1 for m in messages if m.role == 'user')
        assistant_msgs = sum(1 for m in messages if m.role == 'assistant')
        system_msgs = sum(1 for m in messages if m.role == 'system')
        
        print(f"\nMessage Breakdown:")
        print(f"  User messages: {user_msgs}")
        print(f"  Assistant messages: {assistant_msgs}")
        print(f"  System messages: {system_msgs}")
        
        # Conversation lengths
        if participants:
            conv_lengths = []
            for p in participants:
                msg_count = Message.query.filter_by(
                    participant_id=p.participant_id
                ).filter(Message.role != 'system').count()
                conv_lengths.append(msg_count)
            
            print(f"\nConversation Lengths (excluding system):")
            print(f"  Average: {sum(conv_lengths)/len(conv_lengths):.1f} messages")
            print(f"  Min: {min(conv_lengths)} messages")
            print(f"  Max: {max(conv_lengths)} messages")
        
        # Recent activity
        if participants:
            most_recent = max(participants, key=lambda p: p.updated_at)
            print(f"\nMost Recent Activity:")
            print(f"  Participant: {most_recent.participant_id}")
            print(f"  Time: {most_recent.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n" + "="*60 + "\n")


def list_participants():
    """List all participants with basic info."""
    app = create_app()
    with app.app_context():
        participants = Participant.query.order_by(Participant.created_at).all()
        
        print("\n" + "="*80)
        print("PARTICIPANTS LIST")
        print("="*80)
        print(f"{'ID':<20} {'Condition':<30} {'Messages':<10} {'Created':<20}")
        print("-"*80)
        
        for p in participants:
            msg_count = Message.query.filter_by(
                participant_id=p.participant_id
            ).filter(Message.role != 'system').count()
            
            print(f"{p.participant_id:<20} {p.condition_name:<30} {msg_count:<10} "
                  f"{p.created_at.strftime('%Y-%m-%d %H:%M'):<20}")
        
        print("="*80 + "\n")


def view_conversation(participant_id):
    """View a specific participant's conversation."""
    app = create_app()
    with app.app_context():
        participant = Participant.query.get(participant_id)
        
        if not participant:
            print(f"❌ Participant '{participant_id}' not found.")
            return
        
        messages = Message.query.filter_by(
            participant_id=participant_id
        ).order_by(Message.timestamp).all()
        
        print("\n" + "="*80)
        print(f"CONVERSATION: {participant_id}")
        print(f"Condition: {participant.condition_name}")
        print(f"Started: {participant.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80 + "\n")
        
        for msg in messages:
            if msg.role == 'system':
                print(f"[SYSTEM PROMPT]")
                print(f"{msg.content}\n")
            elif msg.role == 'user':
                print(f"USER ({msg.timestamp.strftime('%H:%M:%S')}):")
                print(f"  {msg.content}\n")
            elif msg.role == 'assistant':
                print(f"ASSISTANT ({msg.timestamp.strftime('%H:%M:%S')}):")
                print(f"  {msg.content}\n")
        
        print("="*80 + "\n")


def delete_participant(participant_id, confirm=False):
    """Delete a participant and all their messages."""
    app = create_app()
    with app.app_context():
        participant = Participant.query.get(participant_id)
        
        if not participant:
            print(f"❌ Participant '{participant_id}' not found.")
            return
        
        msg_count = Message.query.filter_by(participant_id=participant_id).count()
        
        if not confirm:
            print(f"⚠️  This will delete participant '{participant_id}' and {msg_count} messages.")
            print("   Run with --confirm flag to proceed.")
            return
        
        db.session.delete(participant)
        db.session.commit()
        
        print(f"✅ Deleted participant '{participant_id}' and {msg_count} messages.")


def clear_all_data(confirm=False):
    """Clear all data from the database."""
    app = create_app()
    with app.app_context():
        participant_count = Participant.query.count()
        message_count = Message.query.count()
        
        if not confirm:
            print(f"⚠️  This will delete ALL data:")
            print(f"   - {participant_count} participants")
            print(f"   - {message_count} messages")
            print("   Run with --confirm flag to proceed.")
            return
        
        Message.query.delete()
        Participant.query.delete()
        db.session.commit()
        
        print(f"✅ Cleared all data: {participant_count} participants, {message_count} messages.")


def main():
    parser = argparse.ArgumentParser(description='Database utilities for experimental chat')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Export commands
    export_json = subparsers.add_parser('export-json', help='Export data to JSON')
    export_json.add_argument('--output', default='data/export_data.json', help='Output filename')
    
    export_csv = subparsers.add_parser('export-csv', help='Export messages to CSV (one row per message)')
    export_csv.add_argument('--output', default='data/export_messages.csv', help='Output filename')
    
    export_convos = subparsers.add_parser('export-conversations', help='Export conversations to CSV (one row per participant)')
    export_convos.add_argument('--output', default='data/conversations.csv', help='Output filename')
    
    # View commands
    subparsers.add_parser('stats', help='Show database statistics')
    subparsers.add_parser('list', help='List all participants')
    
    view = subparsers.add_parser('view', help='View a conversation')
    view.add_argument('participant_id', help='Participant ID to view')
    
    # Delete commands
    delete = subparsers.add_parser('delete', help='Delete a participant')
    delete.add_argument('participant_id', help='Participant ID to delete')
    delete.add_argument('--confirm', action='store_true', help='Confirm deletion')
    
    clear = subparsers.add_parser('clear', help='Clear all data')
    clear.add_argument('--confirm', action='store_true', help='Confirm deletion')
    
    args = parser.parse_args()
    
    if args.command == 'export-json':
        export_to_json(args.output)
    elif args.command == 'export-csv':
        export_to_csv(args.output)
    elif args.command == 'export-conversations':
        export_conversations_csv(args.output)
    elif args.command == 'stats':
        get_statistics()
    elif args.command == 'list':
        list_participants()
    elif args.command == 'view':
        view_conversation(args.participant_id)
    elif args.command == 'delete':
        delete_participant(args.participant_id, args.confirm)
    elif args.command == 'clear':
        clear_all_data(args.confirm)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()