"""
NeuroAid AI Chatbot Service
============================
REAL AI-powered chatbot using trained LLM model.
This service integrates the actual AI workflow with LangGraph.

IMPORTANT: This service uses the TRAINED AI MODEL, NOT hardcoded responses.
"""

import sys
import os

# Fix Windows encoding issues - MUST BE FIRST
if sys.platform == 'win32':
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Add the ai/chatbot directory to Python path to import the AI modules
chatbot_ai_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ai', 'chatbot'))
if chatbot_ai_path not in sys.path:
    sys.path.insert(0, chatbot_ai_path)

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from datetime import datetime
import json

# Import the REAL AI workflow components
try:
    from workflow import Workflow
    from models import State
    AI_AVAILABLE = True
    print("✅ AI Chatbot Workflow loaded successfully")
except Exception as e:
    AI_AVAILABLE = False
    print(f"❌ Failed to load AI Chatbot Workflow: {e}")
    print("⚠️ Service will return errors instead of static responses")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize the AI workflow
workflow = Workflow() if AI_AVAILABLE else None

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK' if AI_AVAILABLE else 'ERROR',
        'service': 'NeuroAid AI Chatbot Service',
        'ai_model_loaded': AI_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    REAL AI Chat endpoint - Uses trained LLM model via workflow

    Expected input:
    {
        "message": "user question",
        "history": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    }

    Returns: Non-streaming JSON response with AI-generated answer
    """
    try:
        # Check if AI model is available
        if not AI_AVAILABLE:
            return jsonify({
                'error': 'AI model not loaded',
                'message': 'The trained AI model could not be loaded. Please check server configuration and ensure all dependencies are installed.',
                'details': 'Missing workflow.py, models.py, agents.py, or required packages'
            }), 503

        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({
                'error': 'Message is required',
                'message': 'Please provide a message field in the request body'
            }), 400

        user_message = data['message']
        conversation_history = data.get('history', [])

        # Prepare state for AI workflow
        initial_state = {
            "messages": conversation_history,
            "query": user_message,
            "rewritten_query": None,
            "response": None,
        }

        # Run the AI workflow synchronously (collect all chunks)
        full_response = ""
        try:
            # Use the streaming workflow but collect all chunks
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            async def get_full_response():
                response_text = ""
                async for chunk in workflow.run_streaming(initial_state):
                    if chunk:
                        response_text += chunk
                return response_text

            full_response = loop.run_until_complete(get_full_response())
            loop.close()

        except Exception as model_error:
            # If the model fails, return error (DO NOT use fallback text)
            return jsonify({
                'error': 'AI model inference failed',
                'message': f'The trained model could not generate a response: {str(model_error)}',
                'details': 'Check that OPENAI_API_KEY is set in .env file'
            }), 500

        # Validate that we got a response from the model
        if not full_response or full_response.strip() == "":
            return jsonify({
                'error': 'Empty model response',
                'message': 'The AI model returned an empty response. This may indicate a configuration issue.',
            }), 500

        return jsonify({
            'response': full_response.strip(),
            'timestamp': datetime.now().isoformat(),
            'service': 'ai_chatbot',
            'model': 'gpt-4o-mini',
            'source': 'trained_ai_workflow'
        })

    except Exception as e:
        return jsonify({
            'error': 'Server error',
            'message': str(e)
        }), 500

@app.route('/chat/stream', methods=['POST'])
def chat_stream():
    """
    REAL AI Streaming Chat endpoint - Uses trained LLM model via workflow

    Returns: Server-Sent Events (SSE) stream with real-time AI responses
    """
    try:
        if not AI_AVAILABLE:
            def error_stream():
                error_data = json.dumps({
                    "error": "AI model not loaded",
                    "message": "The trained AI model could not be loaded."
                })
                yield f"data: {error_data}\n\n"

            return Response(
                error_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Access-Control-Allow-Origin": "*"
                }
            )

        data = request.get_json()

        if not data or 'message' not in data:
            def error_stream():
                error_data = json.dumps({"error": "Message is required"})
                yield f"data: {error_data}\n\n"

            return Response(error_stream(), media_type="text/event-stream")

        user_message = data['message']
        conversation_history = data.get('history', [])

        # Prepare state for AI workflow
        initial_state = {
            "messages": conversation_history,
            "query": user_message,
            "rewritten_query": None,
            "response": None,
        }

        async def generate():
            try:
                # Stream chunks from the REAL AI model
                async for chunk in workflow.run_streaming(initial_state):
                    if chunk:
                        data = json.dumps({"chunk": chunk})
                        yield f"data: {data}\n\n"

                # Send completion signal
                yield f"data: {json.dumps({'done': True})}\n\n"

            except Exception as e:
                error_data = json.dumps({
                    "error": "AI model inference failed",
                    "message": str(e)
                })
                yield f"data: {error_data}\n\n"

        # Convert async generator to sync for Flask
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        def sync_generate():
            async_gen = generate()
            while True:
                try:
                    chunk = loop.run_until_complete(async_gen.__anext__())
                    yield chunk
                except StopAsyncIteration:
                    break

        return Response(
            sync_generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*"
            }
        )

    except Exception as e:
        def error_stream():
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"

        return Response(error_stream(), media_type="text/event-stream")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"\n{'='*60}")
    print(f"🤖 NeuroAid AI Chatbot Service (REAL AI MODEL)")
    print(f"{'='*60}")
    print(f"📍 Running on: http://localhost:{port}")
    print(f"📍 Health check: http://localhost:{port}/health")
    print(f"📍 Chat endpoint: POST http://localhost:{port}/chat")
    print(f"📍 Streaming endpoint: POST http://localhost:{port}/chat/stream")
    print(f"🧠 AI Model: {'LOADED ✅' if AI_AVAILABLE else 'NOT LOADED ❌'}")
    print(f"{'='*60}\n")

    if not AI_AVAILABLE:
        print("⚠️  WARNING: AI model not loaded. Service will return errors.")
        print("⚠️  Check that ai/chatbot directory contains workflow.py and models.py")
        print("⚠️  Check that OPENAI_API_KEY is set in .env file\n")

    app.run(host='0.0.0.0', port=port, debug=True)
