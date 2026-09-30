"""
Chatbot routes
"""

from flask import Blueprint, request, jsonify, current_app
from extensions import db
from models.chatbot import ChatbotKnowledge
from models.event import Event
from models.news import News
from middleware.auth import admin_required
from openai import OpenAI
import os

chatbot_bp = Blueprint('chatbot', __name__)

# Initialize OpenAI client (will be set in route handlers)
openai_client = None

def get_knowledge_base_context():
    """Build knowledge base from database and static content"""
    context_parts = []
    
    # Get events information
    events = Event.query.filter_by(is_jubilee_event=True).all()
    if events:
        context_parts.append("## Platinum Jubilee Events:")
        for event in events:
            context_parts.append(f"- {event.title}: {event.description or 'No description'}")
            if event.start_date:
                context_parts.append(f"  Date: {event.start_date.strftime('%Y-%m-%d %H:%M')}")
            if event.location:
                context_parts.append(f"  Location: {event.location}")
    
    # Get recent news
    news = News.query.filter_by(is_published=True).order_by(News.published_at.desc()).limit(5).all()
    if news:
        context_parts.append("\n## Recent Announcements:")
        for article in news:
            context_parts.append(f"- {article.title}: {article.content[:200]}...")
    
    # Get knowledge base entries
    kb_entries = ChatbotKnowledge.query.all()
    if kb_entries:
        context_parts.append("\n## Frequently Asked Questions:")
        for entry in kb_entries:
            context_parts.append(f"Q: {entry.question}")
            context_parts.append(f"A: {entry.answer}")
    
    # Static information
    static_info = """
## How to Register:
1. Click on the "Register" button on the homepage
2. Fill in your email, password, and basic information
3. Verify your email/mobile number
4. Complete your profile with batch year, profession, etc.
5. Wait for admin approval

## How to Join Events:
1. Browse events from the Events page
2. Click on an event you want to attend
3. Click "Register" button
4. You'll receive a QR code for check-in
5. Present the QR code at the event venue

## Alumni Directory Usage:
1. Go to the Alumni Directory page
2. Use search filters: name, batch year, profession, location
3. Click on an alumni profile to view details
4. Contact information is visible only to logged-in users

## Donation Information:
1. Go to the Donations page
2. Fill in your details and donation amount
3. Submit the form
4. Admin will process and update the status
5. You can track your donation status

## Platinum Jubilee Schedule:
Check the Events page for the complete schedule of Platinum Jubilee celebrations.
All jubilee events are marked with a special badge.
"""
    context_parts.append(static_info)
    
    return "\n".join(context_parts)

@chatbot_bp.route('/query', methods=['POST'])
def chatbot_query():
    """Handle chatbot query"""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    # Get OpenAI API key from config
    api_key = current_app.config.get('OPENAI_API_KEY')
    if not api_key:
        # Fallback response without OpenAI
        return jsonify({
            'response': 'Chatbot is not configured. Please contact admin.',
            'sources': []
        }), 200
    
    # Initialize client if needed
    global openai_client
    if not openai_client:
        openai_client = OpenAI(api_key=api_key)
    
    try:
        # Get knowledge base context
        context = get_knowledge_base_context()
        
        # Build prompt
        system_prompt = """You are a helpful assistant for the Alumni Website. 
Answer questions based ONLY on the provided context about:
- How to register and use the website
- How to join events
- Alumni directory usage
- Platinum Jubilee schedule and events
- Donation information
- General website features

If the question cannot be answered from the context, politely say you don't have that information and suggest contacting the admin.

Keep responses concise and helpful."""
        
        user_prompt = f"""Context:
{context}

User Question: {query}

Answer the question based on the context above:"""
        
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        
        return jsonify({
            'response': answer,
            'sources': ['website_data', 'knowledge_base']
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to process query',
            'message': str(e)
        }), 500

@chatbot_bp.route('/query-whatsapp', methods=['POST'])
def chatbot_query_whatsapp():
    """WhatsApp API endpoint for chatbot"""
    data = request.get_json()
    query = data.get('query', '').strip()
    phone_number = data.get('phone_number', '')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    # Get OpenAI API key from config
    api_key = current_app.config.get('OPENAI_API_KEY')
    if not api_key:
        return jsonify({
            'message': 'Chatbot is not configured. Please contact admin.',
            'phone_number': phone_number
        }), 200
    
    # Initialize client if needed
    global openai_client
    if not openai_client:
        openai_client = OpenAI(api_key=api_key)
    
    try:
        context = get_knowledge_base_context()
        system_prompt = """You are a helpful assistant for the Alumni Website. 
Answer questions based ONLY on the provided context about:
- How to register and use the website
- How to join events
- Alumni directory usage
- Platinum Jubilee schedule and events
- Donation information
- General website features

If the question cannot be answered from the context, politely say you don't have that information and suggest contacting the admin.

Keep responses concise and helpful."""
        
        user_prompt = f"""Context:
{context}

User Question: {query}

Answer the question based on the context above:"""
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        
        return jsonify({
            'message': answer,
            'phone_number': phone_number
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Sorry, I could not process your query. Please try again later.',
            'phone_number': phone_number
        }), 200

@chatbot_bp.route('/knowledge', methods=['POST'])
@admin_required
def add_knowledge():
    """Add knowledge base entry (admin only)"""
    data = request.get_json()
    
    required_fields = ['category', 'question', 'answer']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    entry = ChatbotKnowledge(
        category=data['category'],
        question=data['question'],
        answer=data['answer'],
        source_type=data.get('source_type', 'static'),
        source_id=data.get('source_id')
    )
    
    db.session.add(entry)
    db.session.commit()
    
    return jsonify({
        'message': 'Knowledge entry added successfully',
        'entry': entry.to_dict()
    }), 201

@chatbot_bp.route('/knowledge', methods=['GET'])
@admin_required
def list_knowledge():
    """List knowledge base entries (admin only)"""
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = ChatbotKnowledge.query
    
    if category:
        query = query.filter(ChatbotKnowledge.category == category)
    
    query = query.order_by(ChatbotKnowledge.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    entries = [entry.to_dict() for entry in pagination.items]
    
    return jsonify({
        'entries': entries,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200
