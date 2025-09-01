"""
Token tracking system for JR AI Control
Tracks token usage per message and total usage across sessions
"""

import json
import os
import tiktoken
from typing import Dict, Optional

class TokenTracker:
    def __init__(self):
        self.total_tokens = 0
        self.message_tokens = {}
        self.token_file = "token_usage.json"
        self.load_token_data()
    
    def load_token_data(self):
        """Load token usage data from file"""
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as f:
                    data = json.load(f)
                    self.total_tokens = data.get('total_tokens', 0)
                    self.message_tokens = data.get('message_tokens', {})
        except Exception as e:
            print(f"Error loading token data: {e}")
            self.total_tokens = 0
            self.message_tokens = {}
    
    def save_token_data(self):
        """Save token usage data to file"""
        try:
            data = {
                'total_tokens': self.total_tokens,
                'message_tokens': self.message_tokens
            }
            with open(self.token_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving token data: {e}")
    
    def count_tokens(self, text: str, model: str = "gpt-3.5-turbo") -> int:
        """
        Count tokens in text using tiktoken
        For Gemini models, we'll use a rough approximation
        """
        try:
            # For Gemini models, use a rough approximation (4 chars per token)
            if "gemini" in model.lower():
                return len(text) // 4
            
            # For other models, try to use tiktoken
            try:
                encoding = tiktoken.encoding_for_model(model)
                return len(encoding.encode(text))
            except:
                # Fallback to rough approximation
                return len(text) // 4
                
        except Exception as e:
            print(f"Error counting tokens: {e}")
            # Fallback: rough approximation (4 characters per token)
            return len(text) // 4
    
    def track_message(self, message_id: str, input_text: str, output_text: str, model: str = "gemini") -> int:
        """Track tokens for a specific message exchange"""
        input_tokens = self.count_tokens(input_text, model)
        output_tokens = self.count_tokens(output_text, model)
        total_message_tokens = input_tokens + output_tokens
        
        # Store message tokens
        self.message_tokens[message_id] = {
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': total_message_tokens,
            'model': model
        }
        
        # Update total
        self.total_tokens += total_message_tokens
        
        # Save to file
        self.save_token_data()
        
        return total_message_tokens
    
    def get_message_tokens(self, message_id: str) -> Optional[Dict]:
        """Get token information for a specific message"""
        return self.message_tokens.get(message_id)
    
    def get_total_tokens(self) -> int:
        """Get total token usage across all sessions"""
        return self.total_tokens
    
    def reset_total_tokens(self):
        """Reset total token counter"""
        self.total_tokens = 0
        self.save_token_data()
    
    def get_session_stats(self) -> Dict:
        """Get statistics for current session"""
        session_tokens = sum(
            msg['total_tokens'] for msg in self.message_tokens.values()
        )
        
        return {
            'session_tokens': session_tokens,
            'total_tokens': self.total_tokens,
            'messages_count': len(self.message_tokens)
        }

# Global token tracker instance
_token_tracker = None

def get_token_tracker() -> TokenTracker:
    """Get the global token tracker instance"""
    global _token_tracker
    if _token_tracker is None:
        _token_tracker = TokenTracker()
    return _token_tracker

def track_message_tokens(message_id: str, input_text: str, output_text: str, model: str = "gemini") -> int:
    """Convenience function to track message tokens"""
    tracker = get_token_tracker()
    return tracker.track_message(message_id, input_text, output_text, model)

def get_total_token_usage() -> int:
    """Convenience function to get total token usage"""
    tracker = get_token_tracker()
    return tracker.get_total_tokens()