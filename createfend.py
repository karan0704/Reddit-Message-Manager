import os

def create_templates():
    base_path = "D:\\Karan Ticket Project\\Reddit Message Manager"

    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(base_path, "src\\main\\resources\\templates")
    os.makedirs(templates_dir, exist_ok=True)

    templates = [
        {
            "name": "index.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reddit Message Manager</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #ff4500 0%, #ff6b35 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 400px;
        }
        h1 { color: #333; margin-bottom: 20px; }
        .login-btn {
            display: inline-block;
            background-color: #ff4500;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }
        .login-btn:hover { background-color: #e03d00; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📧 Reddit Message Manager</h1>
        <p>Manage your Reddit messages with ease</p>
        <div th:if="${message}" th:text="${message}" style="color: green; margin: 20px 0;"></div>
        <a href="/login" class="login-btn">🔑 Login with Reddit</a>
    </div>
</body>
</html>"""
        },

        {
            "name": "dashboard.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Reddit Message Manager</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            border-bottom: 1px solid #eee;
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .welcome { color: #333; margin: 0; }
        .username { color: #ff4500; font-weight: bold; }
        .controls {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            text-decoration: none;
            text-align: center;
            display: inline-block;
        }
        .btn-primary { background-color: #ff4500; color: white; }
        .btn-primary:hover { background-color: #e03d00; }
        .btn-secondary { background-color: #0079d3; color: white; }
        .btn-secondary:hover { background-color: #006bb3; }
        .search-section {
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
        }
        .search-input {
            width: 70%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-right: 10px;
        }
        .messages-container {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
            min-height: 200px;
        }
        .message {
            background: white;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ff4500;
        }
        .loading { text-align: center; color: #666; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1 class="welcome">Reddit Message Manager</h1>
                <p>Welcome, <span class="username" th:text="${username}">User</span>!</p>
            </div>
            <a href="/logout" class="btn btn-secondary">Logout</a>
        </div>
        
        <div class="controls">
            <button onclick="loadMessages('inbox')" class="btn btn-primary">Load Inbox</button>
            <button onclick="loadMessages('unread')" class="btn btn-primary">Load Unread</button>
            <button onclick="loadMessages('sent')" class="btn btn-primary">Load Sent Messages</button>
            <button onclick="getStats()" class="btn btn-secondary">Message Statistics</button>
        </div>
        
        <div class="search-section">
            <h3>Search Messages</h3>
            <input type="text" id="searchInput" class="search-input" placeholder="Search your messages...">
            <button onclick="searchMessages()" class="btn btn-primary">Search</button>
            <button onclick="searchRedditPosts()" class="btn btn-secondary">Search Reddit Posts</button>
        </div>
        
        <div id="messages" class="messages-container">
            <p class="loading">Click a button above to load your Reddit messages...</p>
        </div>
    </div>

    <script>
        async function loadMessages(type) {
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = '<p class="loading">Loading ' + type + ' messages...</p>';
            
            try {
                const response = await fetch(`/api/messages/${type}?refresh=true`);
                const data = await response.json();
                
                if (response.ok) {
                    displayMessages(data.messages, type);
                } else {
                    messagesDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
                }
            } catch (error) {
                console.error('Error:', error);
                messagesDiv.innerHTML = '<p style="color: red;">Failed to load messages</p>';
            }
        }
        
        async function searchMessages() {
            const query = document.getElementById('searchInput').value;
            if (!query.trim()) {
                alert('Please enter a search term');
                return;
            }
            
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = '<p class="loading">Searching messages...</p>';
            
            try {
                const response = await fetch(`/api/search/messages?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                
                if (response.ok) {
                    displayMessages(data.messages, 'search results');
                } else {
                    messagesDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
                }
            } catch (error) {
                messagesDiv.innerHTML = '<p style="color: red;">Search failed</p>';
            }
        }
        
        async function searchRedditPosts() {
            const query = document.getElementById('searchInput').value;
            if (!query.trim()) {
                alert('Please enter a search term');
                return;
            }
            
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = '<p class="loading">Searching Reddit posts...</p>';
            
            try {
                const response = await fetch(`/api/search/posts?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                
                if (response.ok) {
                    displaySearchResults(data);
                } else {
                    messagesDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
                }
            } catch (error) {
                messagesDiv.innerHTML = '<p style="color: red;">Reddit search failed</p>';
            }
        }
        
        async function getStats() {
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = '<p class="loading">Loading statistics...</p>';
            
            try {
                const response = await fetch('/api/messages/stats');
                const data = await response.json();
                
                if (response.ok) {
                    messagesDiv.innerHTML = `
                        <h3>Message Statistics</h3>
                        <div class="message">
                            <h4>Your Reddit Message Summary</h4>
                            <p>${data.statistics.body}</p>
                        </div>
                    `;
                } else {
                    messagesDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
                }
            } catch (error) {
                messagesDiv.innerHTML = '<p style="color: red;">Failed to load statistics</p>';
            }
        }
        
        function displayMessages(messages, type) {
            const messagesDiv = document.getElementById('messages');
            
            if (!messages || messages.length === 0) {
                messagesDiv.innerHTML = `<p>No ${type} messages found.</p>`;
                return;
            }
            
            let html = `<h3>${type.charAt(0).toUpperCase() + type.slice(1)} Messages (${messages.length})</h3>`;
            
            messages.forEach(message => {
                html += `
                    <div class="message">
                        <h4>${message.subject || 'No Subject'}</h4>
                        <p><strong>From:</strong> ${message.author || 'Unknown'}</p>
                        <p><strong>Date:</strong> ${message.redditCreatedAt ? new Date(message.redditCreatedAt).toLocaleString() : 'Unknown'}</p>
                        <p>${message.body ? message.body.substring(0, 200) + (message.body.length > 200 ? '...' : '') : 'No content'}</p>
                        ${message.subreddit ? `<p><strong>Subreddit:</strong> r/${message.subreddit}</p>` : ''}
                    </div>
                `;
            });
            
            messagesDiv.innerHTML = html;
        }
        
        function displaySearchResults(data) {
            const messagesDiv = document.getElementById('messages');
            
            if (!data.posts || data.posts.length === 0) {
                messagesDiv.innerHTML = '<p>No Reddit posts found.</p>';
                return;
            }
            
            let html = `<h3>Reddit Search Results (${data.totalResults})</h3>`;
            
            data.posts.forEach(postData => {
                const post = postData.data;
                html += `
                    <div class="message">
                        <h4>${post.title}</h4>
                        <p><strong>Subreddit:</strong> r/${post.subreddit}</p>
                        <p><strong>Author:</strong> ${post.author}</p>
                        <p><strong>Score:</strong> ${post.score}</p>
                        <a href="https://reddit.com${post.permalink}" target="_blank" class="btn btn-secondary">View Post</a>
                    </div>
                `;
            });
            
            messagesDiv.innerHTML = html;
        }
    </script>
</body>
</html>"""
        },

        {
            "name": "error.html",
            "content": """<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - Reddit Message Manager</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        .error-container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
        }
        h1 { color: #d32f2f; margin-bottom: 20px; }
        .error-message { color: #666; margin-bottom: 30px; }
        .btn {
            display: inline-block;
            background-color: #ff4500;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }
        .btn:hover { background-color: #e03d00; }
    </style>
</head>
<body>
    <div class="error-container">
        <h1>⚠️ Error</h1>
        <p class="error-message" th:text="${errorMessage}">Something went wrong</p>
        <a href="/" class="btn">Go Home</a>
    </div>
</body>
</html>"""
        }
    ]

    # Create template files
    for template in templates:
        file_path = os.path.join(templates_dir, template["name"])
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(template["content"])
            print(f"✓ Created: {template['name']}")
        except Exception as e:
            print(f"✗ Failed to create {template['name']}: {e}")

    print(f"\n✅ Templates created in: {templates_dir}")
    print("\nYour application should now work! Try accessing:")
    print("• http://localhost:8080 - Home page")
    print("• http://localhost:8080/login - Reddit login")
    print("• http://localhost:8080/dashboard - Dashboard (after login)")

if __name__ == "__main__":
    create_templates()
