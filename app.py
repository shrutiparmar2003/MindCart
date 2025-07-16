import streamlit as st
import google.generativeai as genai
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
import time

# Configure Streamlit page
st.set_page_config(
    page_title="🧠 MindCart - Shop Smarter, Live Better",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern design
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #f0fdf4 0%, #fafafa 100%);
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }

    .product-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #10b981;
    }

    .cart-item {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #3b82f6;
    }

    .analysis-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }

    .keep-item { border-left-color: #10b981; }
    .reconsider-item { border-left-color: #f59e0b; }
    .optional-item { border-left-color: #8b5cf6; }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
    }

    .identity-badge {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(102, 126, 234, 0.3);
    }

    .justified-item {
        background: #d1fae5;
        border-left-color: #10b981;
    }

    .improvement-message {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
    }

    .tip-card {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'landing'
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'session_history' not in st.session_state:
        st.session_state.session_history = []
    if 'shopping_goal' not in st.session_state:
        st.session_state.shopping_goal = None
    if 'justified_items' not in st.session_state:
        st.session_state.justified_items = {}
    if 'show_justification' not in st.session_state:
        st.session_state.show_justification = {}

init_session_state()

# Configure Gemini API (uncomment and add your API key)
genai.configure(api_key="Your api key here")

# Sample products database
PRODUCTS = {
    "🥛 Milk": {"category": "Essential", "price": 60, "emoji": "🥛"},
    "🍫 Chocolate Cake": {"category": "Treat", "price": 350, "emoji": "🍫"},
    "⌚ Smartwatch": {"category": "Luxury", "price": 15000, "emoji": "⌚"},
    "🍎 Apples": {"category": "Essential", "price": 120, "emoji": "🍎"},
    "🍕 Pizza": {"category": "Treat", "price": 450, "emoji": "🍕"},
    "👕 T-Shirt": {"category": "Essential", "price": 800, "emoji": "👕"},
    "🎮 Gaming Console": {"category": "Luxury", "price": 50000, "emoji": "🎮"},
    "🧴 Shampoo": {"category": "Essential", "price": 250, "emoji": "🧴"},
    "🍿 Popcorn": {"category": "Treat", "price": 100, "emoji": "🍿"},
    "📱 Phone Case": {"category": "Impulse", "price": 500, "emoji": "📱"},
    "🧸 Teddy Bear": {"category": "Impulse", "price": 1200, "emoji": "🧸"},
    "☕ Coffee": {"category": "Essential", "price": 150, "emoji": "☕"},
    "💄 Lipstick": {"category": "Impulse", "price": 800, "emoji": "💄"},
    "🏃‍♀️ Running Shoes": {"category": "Essential", "price": 3500, "emoji": "🏃‍♀️"},
    "🍰 Cupcakes": {"category": "Treat", "price": 200, "emoji": "🍰"}
}

def analyze_cart_with_gemini(cart_items, shopping_goal=None):
    """Analyze cart using Gemini API"""
    try:
        # Initialize the model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Create prompt for Gemini
        cart_details = []
        for item in cart_items:
            product = PRODUCTS[item["name"]]
            cart_details.append({
                "name": item["name"],
                "price": product["price"],
                "category": product["category"],
                "reason": item.get("reason", "No reason provided")
            })

        prompt = f"""
        You are a shopping psychology expert analyzing a customer's cart.
        Shopping Goal: {shopping_goal or "General Shopping"}

        Cart Items:
        {json.dumps(cart_details, indent=2)}

        For each item, provide:
        1. A verdict: "✅ Keep", "⚠️ Reconsider", or "🤔 Optional"
        2. A personalized suggestion based on behavioral psychology
        3. Consider the shopping goal and item necessity

        Also provide:
        - Shopping identity badge (e.g., "Mindful Shopper", "Impulse Buyer", "Balanced Shopper")
        - Personality breakdown (mindful %, indulgent %, emotional %)
        - Estimated savings if flagged items are removed
        - **Reward Recommendation**: If the customer removes impulse or luxury items, suggest a positive reinforcement message that includes:
        - A sense of achievement (e.g., "Great job cutting down!")
        - A small, affordable treat suggestion (e.g., "Would you like to treat yourself with a healthy snack instead?")
        - Ensure that this reward keeps the overall cart value reasonable without promoting overspending.

        Return response in this exact JSON format:
        {{
            "items": [
                {{
                    "name": "item_name",
                    "verdict": "verdict",
                    "suggestion": "detailed_suggestion"
                }}
            ],
            "summary": {{
                "identity_badge": "badge_name",
                "estimated_savings": savings_amount
                "reward_recommendation": "reward_text"
            }},
            "personality": {{
                "mindful": percentage,
                "indulgent": percentage,
                "emotional": percentage
            }}
        }}
        """

        # Call Gemini API
        response = model.generate_content(prompt)

        # Parse the response
        try:
            # Extract JSON from response
            response_text = response.text
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end]

            gemini_analysis = json.loads(response_text)

            # Build final analysis structure
            analysis = {
                "items": [],
                "summary": {
                    "total_items": len(cart_items),
                    "flagged_items": 0,
                    "estimated_savings": gemini_analysis["summary"]["estimated_savings"],
                    "identity_badge": gemini_analysis["summary"]["identity_badge"]
                },
                "categories": {"Essential": 0, "Treat": 0, "Luxury": 0, "Impulse": 0},
                "personality": gemini_analysis["personality"]
            }

            # Process each item
            for i, item in enumerate(cart_items):
                product = PRODUCTS[item["name"]]
                category = product["category"]
                analysis["categories"][category] += 1

                # Get Gemini analysis for this item
                gemini_item = gemini_analysis["items"][i] if i < len(gemini_analysis["items"]) else {}

                verdict = gemini_item.get("verdict", "🤔 Optional")
                suggestion = gemini_item.get("suggestion", "Consider if this purchase aligns with your goals.")

                if "Reconsider" in verdict:
                    analysis["summary"]["flagged_items"] += 1

                analysis["items"].append({
                    "name": item["name"],
                    "emoji": product["emoji"],
                    "verdict": verdict,
                    "suggestion": suggestion,
                    "price": product["price"],
                    "reason": item.get("reason", "")
                })

            return analysis

        except (json.JSONDecodeError, KeyError) as e:
            st.error(f"Error parsing Gemini response: {e}")
            return create_fallback_analysis(cart_items)

    except Exception as e:
        st.warning(f"Using fallback analysis (Gemini API not configured): {e}")
        return create_fallback_analysis(cart_items)

def create_fallback_analysis(cart_items):
    """Fallback analysis if Gemini API fails"""
    analysis = {
        "items": [],
        "summary": {
            "total_items": len(cart_items),
            "flagged_items": 0,
            "estimated_savings": 0,
            "identity_badge": "Balanced Shopper"
        },
        "categories": {"Essential": 0, "Treat": 0, "Luxury": 0, "Impulse": 0},
        "personality": {"mindful": 70, "indulgent": 20, "emotional": 10}
    }

    total_savings = 0

    for item in cart_items:
        product = PRODUCTS[item["name"]]
        category = product["category"]
        analysis["categories"][category] += 1

        # Basic analysis logic
        if category == "Essential":
            verdict = "✅ Keep"
            suggestion = "This is an essential item for your daily needs."
        elif category == "Treat":
            verdict = "🤔 Optional"
            suggestion = "This is a treat - enjoy responsibly if it fits your budget."
        elif category == "Luxury":
            verdict = "⚠️ Reconsider"
            suggestion = "This is a luxury item. Consider if it's truly necessary right now."
            analysis["summary"]["flagged_items"] += 1
            total_savings += product["price"] * 0.3
        else:  # Impulse
            verdict = "⚠️ Reconsider"
            suggestion = "This seems like an impulse purchase. Take a moment to think."
            analysis["summary"]["flagged_items"] += 1
            total_savings += product["price"]

        analysis["items"].append({
            "name": item["name"],
            "emoji": product["emoji"],
            "verdict": verdict,
            "suggestion": suggestion,
            "price": product["price"],
            "reason": item.get("reason", "")
        })

    analysis["summary"]["estimated_savings"] = total_savings
    return analysis

def landing_page():
    """Landing page with welcome message and CTA"""
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3rem; color: #1f2937; margin-bottom: 1rem;">🧠 MindCart</h1>
        <h2 style="color: #6b7280; margin-bottom: 2rem;">Shop Smarter, Live Better</h2>
        <p style="font-size: 1.2rem; color: #4b5563; margin-bottom: 2rem;">
            AI that helps you think twice before buying – and save smarter!
        </p>
        <h3 style="color: #10b981; margin-bottom: 1rem;">Hi there 👋</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("### 🎯 What's your shopping goal today?")
        goal = st.selectbox(
            "Choose your focus:",
            ["Essentials Only", "Balanced Shopping", "Treat Yourself", "Gift Shopping"],
            key="shopping_goal_selector"
        )

        if st.button("🛒 Start Smart Cart", key="start_cart"):
            st.session_state.shopping_goal = goal
            st.session_state.current_page = 'cart_builder'
            st.rerun()

    # Features showcase
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="product-card">
            <h4>🧠 Mindful Analysis</h4>
            <p>AI analyzes your cart using behavioral psychology to help you make smarter decisions.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="product-card">
            <h4>💡 Smart Insights</h4>
            <p>Get personalized suggestions based on your shopping patterns and goals.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="product-card">
            <h4>📊 Progress Tracking</h4>
            <p>Monitor your shopping improvement and develop better buying habits.</p>
        </div>
        """, unsafe_allow_html=True)

def cart_builder_page():
    """Cart builder with product selection and cart management"""
    st.markdown("""
    <div class="main-header">
        <h1>🛒 Build Your Smart Cart</h1>
        <p style="color: #6b7280;">Goal: {}</p>
    </div>
    """.format(st.session_state.shopping_goal), unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🛍️ Available Products")

        # Search/filter functionality
        search_term = st.text_input("🔍 Search products...", placeholder="Type to search...")

        # Filter products based on search
        filtered_products = PRODUCTS
        if search_term:
            filtered_products = {k: v for k, v in PRODUCTS.items()
                               if search_term.lower() in k.lower()}

        # Display products in a grid
        products_per_row = 3
        product_keys = list(filtered_products.keys())

        for i in range(0, len(product_keys), products_per_row):
            cols = st.columns(products_per_row)
            for j, col in enumerate(cols):
                if i + j < len(product_keys):
                    product_name = product_keys[i + j]
                    product_info = filtered_products[product_name]

                    with col:
                        st.markdown(f"""
                        <div class="product-card">
                            <div style="text-align: center; font-size: 2rem;">{product_info['emoji']}</div>
                            <h4>{product_name}</h4>
                            <p style="color: #6b7280;">{product_info['category']}</p>
                            <p style="font-weight: 600; color: #10b981;">₹{product_info['price']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        if st.button(f"➕ Add to Cart", key=f"add_{product_name}"):
                            st.session_state.cart.append({
                                "name": product_name,
                                "price": product_info['price'],
                                "reason": ""
                            })
                            st.success(f"Added {product_name} to cart!")
                            st.rerun()

        # Frequently bought items
        st.markdown("---")
        st.markdown("### 🔄 Frequently Bought by You")
        frequent_items = ["🥛 Milk", "☕ Coffee", "🍎 Apples", "🧴 Shampoo"]

        cols = st.columns(len(frequent_items))
        for i, item in enumerate(frequent_items):
            with cols[i]:
                if st.button(f"Quick Add {PRODUCTS[item]['emoji']}", key=f"quick_{item}"):
                    st.session_state.cart.append({
                        "name": item,
                        "price": PRODUCTS[item]['price'],
                        "reason": "Frequently bought"
                    })
                    st.success(f"Added {item} to cart!")
                    st.rerun()

    with col2:
        st.markdown("### 🛒 Your Cart")

        if st.session_state.cart:
            total_price = 0
            for i, item in enumerate(st.session_state.cart):
                total_price += item['price']

                st.markdown(f"""
                <div class="cart-item">
                    <strong>{item['name']}</strong><br>
                    ₹{item['price']}
                </div>
                """, unsafe_allow_html=True)

                # Optional reason input
                reason = st.text_input(
                    f"Why are you buying this?",
                    value=item.get('reason', ''),
                    key=f"reason_{i}",
                    placeholder="Optional reason..."
                )
                st.session_state.cart[i]['reason'] = reason

                if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()

            st.markdown(f"""
            <div class="metric-card">
                <h3>Total: ₹{total_price}</h3>
                <p>{len(st.session_state.cart)} items</p>
            </div>
            """, unsafe_allow_html=True)

            # Smart upsell banners
            if total_price < 500:
                st.markdown("""
                <div style="background: #fef3c7; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    🛍️ Add ₹{} more to unlock free shipping!
                </div>
                """.format(500 - total_price), unsafe_allow_html=True)

            if total_price >= 800:
                st.markdown("""
                <div style="background: #d1fae5; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    🎁 Great! You qualify for a surprise gift!
                </div>
                """, unsafe_allow_html=True)

            if st.button("🧠 Analyze My Cart", key="analyze_cart"):
                with st.spinner("Analyzing your cart with AI..."):
                    time.sleep(2)  # Simulate API call
                    st.session_state.analysis_result = analyze_cart_with_gemini(st.session_state.cart, st.session_state.shopping_goal)
                    st.session_state.current_page = 'analysis'
                    st.rerun()
        else:
            st.info("Your cart is empty. Add some products to get started!")

    # Navigation
    if st.button("← Back to Home"):
        st.session_state.current_page = 'landing'
        st.rerun()

def analysis_page():
    """Analysis results with AI insights and recommendations"""
    if not st.session_state.analysis_result:
        st.error("No analysis data available. Please build a cart first.")
        return

    analysis = st.session_state.analysis_result

    st.markdown("""
    <div class="main-header">
        <h1>📊 Your Cart Analysis</h1>
        <p style="color: #6b7280;">AI-powered insights for smarter shopping</p>
    </div>
    """, unsafe_allow_html=True)

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Items", analysis["summary"]["total_items"])

    with col2:
        st.metric("Flagged Items", analysis["summary"]["flagged_items"])

    with col3:
        st.metric("Potential Savings", f"₹{analysis['summary']['estimated_savings']:.0f}")

    with col4:
        st.markdown(f"""
        <div class="identity-badge">
            <h4>🏆 Shopping Identity</h4>
            <p>{analysis['summary']['identity_badge']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Category breakdown chart
    st.markdown("### 📈 Cart Category Breakdown")
    categories = analysis["categories"]

    if any(categories.values()):
        fig = px.pie(
            values=list(categories.values()),
            names=list(categories.keys()),
            title="Your Shopping Categories",
            color_discrete_map={
                "Essential": "#10b981",
                "Treat": "#f59e0b",
                "Luxury": "#ef4444",
                "Impulse": "#8b5cf6"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    # Item-by-item analysis
    st.markdown("### 🔍 Item Analysis")

    for item in analysis["items"]:
        item_name = item['name']
        verdict_class = "keep-item" if "Keep" in item["verdict"] else \
                      "reconsider-item" if "Reconsider" in item["verdict"] else "optional-item"

        # Check if item is justified
        if item_name in st.session_state.justified_items:
            verdict_class = "justified-item"

        st.markdown(f"""
        <div class="analysis-card {verdict_class}">
            <h4>{item['emoji']} {item['name']} - ₹{item['price']}</h4>
            <p><strong>{item['verdict']}</strong></p>
            <p>{item['suggestion']}</p>
            {f"<p><em>Your reason: {item['reason']}</em></p>" if item['reason'] else ""}
        </div>
        """, unsafe_allow_html=True)

        # Justify item functionality
        if "Reconsider" in item["verdict"] and item_name not in st.session_state.justified_items:
            col1, col2 = st.columns([1, 3])

            with col1:
                if st.button(f"💭 Justify", key=f"justify_btn_{item_name}"):
                    st.session_state.show_justification[item_name] = True
                    st.rerun()

            # Show justification form if requested
            if st.session_state.show_justification.get(item_name, False):
                with col2:
                    with st.form(key=f"justify_form_{item_name}"):
                        justification = st.text_area(
                            f"Why do you need {item['name']}?",
                            placeholder="Explain your reasoning...",
                            key=f"justification_text_{item_name}"
                        )

                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.form_submit_button("✅ Justify Purchase"):
                                if justification.strip():
                                    st.session_state.justified_items[item_name] = justification
                                    st.session_state.show_justification[item_name] = False
                                    st.success(f"Thanks for explaining! {item['name']} has been justified.")
                                    st.rerun()
                                else:
                                    st.error("Please provide a reason.")

                        with col_b:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state.show_justification[item_name] = False
                                st.rerun()

        # Show justified items
        elif item_name in st.session_state.justified_items:
            st.success(f"✅ Justified: {st.session_state.justified_items[item_name]}")
            if st.button(f"Remove Justification", key=f"remove_justification_{item_name}"):
                del st.session_state.justified_items[item_name]
                st.rerun()

    # Shopping personality
    st.markdown("### 🧠 Your Shopping Personality")
    personality = analysis["personality"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Mindful", f"{personality['mindful']}%")

    with col2:
        st.metric("Indulgent", f"{personality['indulgent']}%")

    with col3:
        st.metric("Emotional", f"{personality['emotional']}%")

    # 10-second reflection pause
    st.markdown("---")
    st.markdown("### ⏱️ Take a Moment to Reflect")

    if st.button("🧘 10-Second Reflection", key="reflection"):
        placeholder = st.empty()
        for i in range(10, 0, -1):
            placeholder.markdown(f"""
            <div style="text-align: center; font-size: 2rem; padding: 2rem;">
                Think about your purchases... {i}
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
        placeholder.markdown("""
        <div style="text-align: center; font-size: 1.5rem; padding: 2rem; color: #10b981;">
            ✨ Reflection complete! You're ready to decide.
        </div>
        """, unsafe_allow_html=True)

    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🛒 Revise Cart"):
            st.session_state.current_page = 'cart_builder'
            st.rerun()

    with col2:
        if st.button("✅ Confirm Order"):
            # Save to history
            st.session_state.session_history.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "items": len(st.session_state.cart),
                "total": sum(item['price'] for item in st.session_state.cart),
                "savings": analysis["summary"]["estimated_savings"],
                "identity": analysis["summary"]["identity_badge"]
            })

            st.success("🎉 Order confirmed! Thank you for shopping mindfully!")
            st.balloons()

            # Reset cart and justifications
            st.session_state.cart = []
            st.session_state.analysis_result = None
            st.session_state.justified_items = {}
            st.session_state.show_justification = {}

            time.sleep(2)
            st.session_state.current_page = 'landing'
            st.rerun()

    with col3:
        if st.button("📜 View History"):
            st.session_state.current_page = 'history'
            st.rerun()
def history_page():
    """Session history with progress tracking"""
    st.markdown("""
    <div class="main-header">
        <h1>📜 Your Shopping History</h1>
        <p style="color: #6b7280;">Track your mindful shopping progress</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.session_history:
        # Progress metrics
        total_sessions = len(st.session_state.session_history)
        total_savings = sum(session['savings'] for session in st.session_state.session_history)
        avg_items = sum(session['items'] for session in st.session_state.session_history) / total_sessions

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Sessions", total_sessions)

        with col2:
            st.metric("Total Savings", f"₹{total_savings:.0f}")

        with col3:
            st.metric("Avg Items/Session", f"{avg_items:.1f}")

        # Progress chart
        st.markdown("### 📈 Savings Progress")

        df = pd.DataFrame(st.session_state.session_history)
        fig = px.line(
            df,
            x='date',
            y='savings',
            title='Your Savings Over Time',
            labels={'savings': 'Savings (₹)', 'date': 'Date'}
        )
        st.plotly_chart(fig, use_container_width=True)

        # Session details
        st.markdown("### 🗂️ Session Details")

        for i, session in enumerate(reversed(st.session_state.session_history)):
            st.markdown(f"""
            <div class="analysis-card">
                <h4>Session {len(st.session_state.session_history) - i}</h4>
                <p><strong>Date:</strong> {session['date']}</p>
                <p><strong>Items:</strong> {session['items']}</p>
                <p><strong>Total:</strong> ₹{session['total']}</p>
                <p><strong>Savings:</strong> ₹{session['savings']:.0f}</p>
                <p><strong>Identity:</strong> {session['identity']}</p>
            </div>
            """, unsafe_allow_html=True)

        # Improvement message
        if total_sessions > 1:
            recent_savings = st.session_state.session_history[-1]['savings']
            prev_savings = st.session_state.session_history[-2]['savings']

            if recent_savings > prev_savings:
                st.success("🎉 You've improved your mindful shopping! Keep it up!")
            else:
                st.info("💡 You're doing great! Remember to take time to reflect before purchasing.")

    else:
        st.info("No shopping history yet. Start shopping to see your progress!")

    # Navigation
    if st.button("← Back to Home"):
        st.session_state.current_page = 'landing'
        st.rerun()

def main():
    """Main application logic"""

    # Navigation
    if st.session_state.current_page == 'landing':
        landing_page()
    elif st.session_state.current_page == 'cart_builder':
        cart_builder_page()
    elif st.session_state.current_page == 'analysis':
        analysis_page()
    elif st.session_state.current_page == 'history':
        history_page()

    # Sidebar for navigation
    with st.sidebar:
        st.markdown("### 🧠 MindCart Navigation")

        if st.button("🏠 Home"):
            st.session_state.current_page = 'landing'
            st.rerun()

        if st.button("🛒 Cart Builder"):
            st.session_state.current_page = 'cart_builder'
            st.rerun()

        if st.button("📜 History"):
            st.session_state.current_page = 'history'
            st.rerun()

        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Take time to reflect before purchasing
        - Consider if items are wants vs needs
        - Set shopping goals before you start
        - Review your patterns in history
        """)


if __name__ == "__main__":
    main()
