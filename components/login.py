import streamlit as st
import time
from components.auth import AuthManager
from components.branding import FCGBranding

class LoginPage:
    """Professional login page for Four Corners Group"""
    
    def __init__(self):
        self.auth_manager = AuthManager()
        
    def show_login_page(self):
        """Display the main login page"""
        # Inject FCG CSS
        FCGBranding.inject_fcg_css()
        
        # Show FCG header
        FCGBranding.show_fcg_header()
        
        # Login form
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            
            st.markdown('<div class="login-header"><h2>🔐 Secure Login</h2></div>', unsafe_allow_html=True)
            
            # Login form
            with st.form("login_form"):
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                login_button = st.form_submit_button("🚀 Login", use_container_width=True)                   
                
                
                if login_button:
                    if username and password:
                        self.handle_login(username, password)
                    else:
                        st.error("Please enter both username and password")
                
                # if forgot_password:
                #     self.show_password_reset_form()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # # Default credentials info
        # self.show_default_credentials()
        
        
    
    def handle_login(self, username: str, password: str):
        """Handle login attempt"""
        # Show loader
        with st.spinner("Authenticating..."):
            FCGBranding.show_fcg_loader("Verifying credentials...")
            time.sleep(1)  # Simulate authentication delay
            
            user_data = self.auth_manager.authenticate_user(username, password)
            
            if user_data:
                # Create session
                session_id = self.auth_manager.create_session(user_data)
                
                # Store in session state
                st.session_state['authenticated'] = True
                st.session_state['session_id'] = session_id
                st.session_state['user_data'] = user_data
                
                # Show success message
                st.success(f"✅ Welcome, {user_data['full_name']}!")
                
                # Redirect to main app
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
    
    # def show_password_reset_form(self):
    #     """Show password reset form"""
    #     st.info("💡 Contact your administrator to reset your password")
    #     st.markdown("""
    #     **Default Credentials:**
    #     - **Admin:** admin / fcg@2024
    #     - **HR Manager:** hr_manager / hr@fcg123
    #     """)
    
    def show_default_credentials(self):
        """Show default credentials for demo purposes"""
        with st.expander("🔑 Demo Credentials (Development Only)"):
            st.markdown("""
            **Administrator Account:**
            - Username: `admin`
            - Password: `fcg@2024`
            - Role: System Administrator
            
            **HR Manager Account:**
            - Username: `hr_manager`
            - Password: `hr@fcg123`
            - Role: HR Manager
            
            > **Note:** These are default credentials for demonstration purposes only.
            > In production, ensure strong passwords and proper security measures.
            """)
    
    def show_user_management(self):
        """Show user management interface (admin only)"""
        if st.session_state.get('user_data', {}).get('role') != 'admin':
            st.error("Access denied. Administrator privileges required.")
            return
        
        st.header("👥 User Management")
        
        with st.expander("➕ Add New User"):
            with st.form("add_user_form"):
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                new_role = st.selectbox("Role", ["hr_manager", "analyst", "admin"])
                new_full_name = st.text_input("Full Name")
                new_email = st.text_input("Email")
                
                if st.form_submit_button("Add User"):
                    if all([new_username, new_password, new_full_name, new_email]):
                        if self.auth_manager.add_user(new_username, new_password, new_role, new_full_name, new_email):
                            st.success(f"✅ User '{new_username}' added successfully!")
                        else:
                            st.error("❌ Username already exists!")
                    else:
                        st.error("Please fill in all fields")
        
        # Change password
        with st.expander("🔒 Change Password"):
            with st.form("change_password_form"):
                old_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("Change Password"):
                    if new_password == confirm_password:
                        username = st.session_state['user_data']['username']
                        if self.auth_manager.change_password(username, old_password, new_password):
                            st.success("✅ Password changed successfully!")
                        else:
                            st.error("❌ Current password is incorrect!")
                    else:
                        st.error("❌ New passwords do not match!")
    
    def logout(self):
        """Handle user logout"""
        if 'session_id' in st.session_state:
            self.auth_manager.logout_user(st.session_state['session_id'])
        
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        st.rerun()