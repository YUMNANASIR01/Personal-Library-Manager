import streamlit as st
import json
import pandas as pd  # Added for genre distribution

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

st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# Sidebar Menu
st.sidebar.title("📚 Menu")
menu_choice = st.sidebar.radio("Choose an action:", [
    "🏠 Home",
    "📖 Add Book",
    "🗑️ Remove Book",
    "🔍 Search Books",
    "📊 Statistics"
])

# Main Content
st.title("📚 Personal Library Manager")

# Home Page
if menu_choice == "🏠 Home":
    st.subheader("🌟 Your Library")
    if not st.session_state.library:
        st.info("📭 Your library is empty. Add some books!")
    else:
        for i, book in enumerate(st.session_state.library, 1):
            status = "✅ Read" if book['read'] else "📖 Unread"
            st.write(f"""
            **{i}. {book['title']}**  
            👤 {book['author']} • 📅 {book['year']} • 🎭 {book['genre']} • {status}
            """)

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
            st.rerun()  # Add refresh after submission

# Remove Book Page (FIXED SECTION)
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
            st.rerun()  # Changed from experimental_rerun() to rerun()
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
                st.write(f"""
                **{book['title']}**  
                👤 {book['author']} • 📅 {book['year']} • 🎭 {book['genre']} • {status}
                """)
        else:
            st.warning("❌ No matching books found")

# Statistics Page
elif menu_choice == "📊 Statistics":
    st.subheader("📊 Library Statistics")
    total = len(st.session_state.library)
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

# Save on exit
save_library()