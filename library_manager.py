
import streamlit as st
import json
import pandas as pd

# Set page config FIRST
st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# Add Tailwind CSS and dark theme (must come after set_page_config)
st.markdown("""

<script src="https://cdn.tailwindcss.com"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.classList.add('dark');
    }
});
</script>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

.dark {
    @apply bg-gray-900 text-white;
}

.stTextInput>div>div>input, .stNumberInput>div>div>input {
    @apply dark:bg-gray-800 dark:text-white dark:border-gray-600 rounded-lg p-2;
}

.stSelectbox>div>div>select {
    @apply dark:bg-gray-800 dark:text-white dark:border-gray-600 rounded-lg p-2;
}

.stRadio>div {
    @apply dark:text-white;
}

.stButton>button {
    @apply dark:bg-blue-600 dark:hover:bg-blue-700 rounded-lg px-4 py-2 text-white;
}

.stMetric {
    @apply dark:bg-gray-800 p-4 rounded-lg;
}

</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'library' not in st.session_state:
    try:
        with open('library.txt', 'r') as f:
            st.session_state.library = json.load(f)
    except FileNotFoundError:
        st.session_state.library = []
    except Exception as e:
        st.error(f"Error loading library: {e}")
        st.session_state.library = []

def save_library():
    try:
        with open('library.txt', 'w') as f:
            json.dump(st.session_state.library, f)
    except Exception as e:
        st.error(f"Error saving library: {e}")

# Main container with max width
st.markdown("""
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
""", unsafe_allow_html=True)

# Sidebar Menu
with st.sidebar:
    st.markdown("""
    <div class="dark:bg-gray-800 p-4 rounded-lg">
        <h1 class="text-2xl font-bold mb-4 dark:text-white">📚 Menu</h1>
    """, unsafe_allow_html=True)
    menu_choice = st.radio("Choose an action:", [
        "🏠 Home",
        "📖 Add Book",
        "🗑️ Remove Book",
        "🔍 Search Books",
        "📊 Statistics"
    ])
    st.markdown("</div>", unsafe_allow_html=True)

# Main Content
st.title("📚 Personal Library Manager")

# Home Page
if menu_choice == "🏠 Home":
    st.subheader("🌟 Your Library")
    if not st.session_state.library:
        st.info("📭 Your library is empty. Add some books!")
    else:
        cols = st.columns(3)
        for i, book in enumerate(st.session_state.library):
            with cols[i % 3]:
                status = "✅ Read" if book['read'] else "📖 Unread"
                st.markdown(f"""
                <div class="dark:bg-gray-800 p-4 rounded-lg mb-4 shadow-lg hover:shadow-xl transition-shadow">
                    <h3 class="text-xl font-bold dark:text-white">{book['title']}</h3>
                    <p class="dark:text-gray-300">👤 {book['author']}</p>
                    <p class="dark:text-gray-300">📅 {book['year']} • 🎭 {book['genre']}</p>
                    <div class="mt-2 px-2 py-1 rounded-full { 'bg-green-600' if book['read'] else 'bg-blue-600' } text-white w-fit">
                        {status}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Add Book Page
elif menu_choice == "📖 Add Book":
    st.subheader("📖 Add New Book")
    with st.form("add_book"):
        title = st.text_input("📘 Title")
        author = st.text_input("👤 Author")
        year = st.number_input("📅 Publication Year", min_value=1800, max_value=2100)
        genre = st.text_input("🎭 Genre")
        read = st.radio("✅ Read Status", ["Yes", "No"])
        submitted = st.form_submit_button("💾 Save Book")
        
        if submitted:
            new_book = {
                'title': title,
                'author': author,
                'year': int(year),
                'genre': genre,
                'read': read == "Yes"
            }
            st.session_state.library.append(new_book)
            save_library()
            st.success("🎉 Book added successfully!")
            st.rerun()

# Remove Book Page
elif menu_choice == "🗑️ Remove Book":
    st.subheader("🗑️ Remove Book")
    if st.session_state.library:
        books = [f"{book['title']} by {book['author']}" for book in st.session_state.library]
        to_remove = st.selectbox("Select book to remove:", books)
        if st.button("❌ Remove"):
            index = books.index(to_remove)
            del st.session_state.library[index]
            save_library()
            st.success("🎉 Book removed successfully!")
            st.rerun()
    else:
        st.info("📭 Your library is empty. Nothing to remove!")

# Search Page
elif menu_choice == "🔍 Search Books":
    st.subheader("🔍 Search Books")
    search_type = st.radio("Search by:", ["📖 Title", "👤 Author"])
    search_term = st.text_input("🔎 Enter search term")
    
    if search_term:
        results = []
        if search_type == "📖 Title":
            results = [book for book in st.session_state.library 
                      if search_term.lower() in book['title'].lower()]
        else:
            results = [book for book in st.session_state.library 
                      if search_term.lower() in book['author'].lower()]
        
        if results:
            st.subheader(f"📚 Found {len(results)} results:")
            for book in results:
                status = "✅ Read" if book['read'] else "📖 Unread"
                st.markdown(f"""
                <div class="dark:bg-gray-800 p-4 rounded-lg mb-4">
                    <h3 class="text-xl font-bold dark:text-white">{book['title']}</h3>
                    <p class="dark:text-gray-300">👤 {book['author']}</p>
                    <p class="dark:text-gray-300">📅 {book['year']} • 🎭 {book['genre']}</p>
                    <div class="mt-2 px-2 py-1 rounded-full { 'bg-green-600' if book['read'] else 'bg-blue-600' } text-white w-fit">
                        {status}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("❌ No matching books found")

# Statistics Page
elif menu_choice == "📊 Statistics":
    st.subheader("📊 Library Statistics")
    total = len(st.session_state.library)
    st.markdown('<div class="stMetric">', unsafe_allow_html=True)
    st.metric("📚 Total Books", total)
    
    if total > 0:
        read_count = sum(1 for book in st.session_state.library if book['read'])
        st.metric("✅ Books Read", f"{read_count} ({read_count/total*100:.1f}%)")
        st.metric("📖 Books Unread", f"{total - read_count} ({(total - read_count)/total*100:.1f}%)")
        
        genres = [book['genre'] for book in st.session_state.library]
        if genres:
            st.write("### 🎭 Genre Distribution")
            st.bar_chart(pd.Series(genres).value_counts())
    else:
        st.info("📭 Your library is empty. Add some books to see statistics!")
    st.markdown('</div>', unsafe_allow_html=True)

# Save on exit
save_library()
