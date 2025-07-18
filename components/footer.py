import streamlit as st

class FCGFooter:
    """Four Corners Group professional footer component"""
    
    @staticmethod
    def get_footer_css():
        """Get CSS styles for the footer"""
        return """
        <style>
        .fcg-footer {
            background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
            color: white;
            padding: 3rem 2rem 1rem 2rem;
            margin-top: 4rem;
            border-radius: 10px 10px 0 0;
            box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.1);
        }
        
        .footer-content {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .footer-section h3 {
            color: #FFD700;
            font-size: 1.2rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        .footer-section p {
            margin: 0.5rem 0;
            line-height: 1.6;
            font-size: 0.9rem;
        }
        
        .footer-section strong {
            color: #E8F5E8;
        }
        
        .footer-logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .footer-logo img {
            width: 60px;
            height: 60px;
        }
        
        .footer-logo-text {
            font-size: 1.1rem;
            font-weight: 700;
            color: #FFD700;
        }
        
        .social-links {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .social-links a {
            display: inline-block;
            width: 40px;
            height: 40px;
            background: #66BB6A;
            border-radius: 50%;
            text-align: center;
            line-height: 40px;
            color: white;
            text-decoration: none;
            transition: background 0.3s ease;
        }
        
        .social-links a:hover {
            background: #FFD700;
            color: #1B5E20;
        }
        
        .footer-bottom {
            text-align: center;
            padding-top: 2rem;
            border-top: 1px solid #66BB6A;
            color: #E8F5E8;
            font-size: 0.9rem;
        }
        
        .contact-info {
            font-size: 0.85rem;
            line-height: 1.5;
        }
        
        .office-section {
            background: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .footer-content {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            
            .fcg-footer {
                padding: 2rem 1rem 1rem 1rem;
            }
        }
        
        @media (max-width: 480px) {
            .footer-content {
                grid-template-columns: 1fr;
            }
            
            .social-links {
                justify-content: center;
            }
        }
        </style>
        """
    
    @staticmethod
    def render_footer():
        """Render the complete FCG footer"""
        # Inject CSS
        st.markdown(FCGFooter.get_footer_css(), unsafe_allow_html=True)
        
        # Footer HTML
        footer_html = """
        <div class="fcg-footer">
            <div class="footer-content">
                <!-- Company Info Section -->
                <div class="footer-section">
                    <div class="footer-logo">
                        <div class="footer-logo-text">Four Corners Group</div>
                    </div>
                    <p><strong>Contact Us</strong></p>
                    <p>Your Partners in Strategic Growth</p>
                    <p>Established 2008</p>
                    <p>Market Research • Business Consulting • Training Solutions</p>
                    
                    <div class="social-links">
                        <a href="#" title="Twitter">🐦</a>
                        <a href="#" title="Facebook">📘</a>
                        <a href="#" title="LinkedIn">💼</a>
                        <a href="#" title="Instagram">📷</a>
                    </div>
                </div>
                
                <!-- Head Office Section -->
                <div class="footer-section">
                    <h3>Head Office (Karachi)</h3>
                    <div class="office-section">
                        <p><strong>Four Corners Group (Pvt.) Ltd.</strong></p>
                        <p>193-K, Block 2m PECHS, Karachi, Pakistan</p>
                        <p><strong>Phone:</strong> +92 21 4312154-5</p>
                        <p><strong>Fax:</strong> +92 21 4312156</p>
                        <p><strong>Email:</strong> info@fourcg.com</p>
                    </div>
                </div>
                
                <!-- Regional Office Rawalpindi -->
                <div class="footer-section">
                    <h3>Regional Office (Rawalpindi)</h3>
                    <div class="office-section">
                        <p><strong>Four Corners Group (Pvt.) Ltd.</strong></p>
                        <p># 99-A/B-2, Block # A, Satellite Town, 6th Road, Rawalpindi, Pakistan</p>
                        <p><strong>Phone:</strong> +92-51-4933002</p>
                        <p><strong>Email:</strong> info@fourcg.com</p>
                    </div>
                </div>
                
                <!-- Regional Office Lahore -->
                <div class="footer-section">
                    <h3>Regional Office (Lahore)</h3>
                    <div class="office-section">
                        <p><strong>Four Corners Group (Pvt.) Ltd.</strong></p>
                        <p>389-C, Block D, Faisal Town, Lahore, Pakistan</p>
                        <p><strong>Phone:</strong> +92 42 35177634</p>
                        <p><strong>Email:</strong> info@fourcg.com</p>
                    </div>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>Copyright © 2025 Four Corners Group Private Limited</p>
                <p>All rights reserved</p>
            </div>
        </div>
        """
        
        st.markdown(footer_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_compact_footer():
        """Render a compact version of the footer for smaller screens"""
        st.markdown(FCGFooter.get_footer_css(), unsafe_allow_html=True)
        
        compact_footer_html = """
        <div class="fcg-footer">
            <div class="footer-content" style="grid-template-columns: 1fr 1fr;">
                <div class="footer-section">
                    <div class="footer-logo">
                        <div class="footer-logo-text">Four Corners Group</div>
                    </div>
                    <p><strong>Your Partners in Strategic Growth</strong></p>
                    <p>Market Research • Business Consulting • Training Solutions</p>
                    
                    <div class="social-links">
                        <a href="#" title="Twitter">🐦</a>
                        <a href="#" title="Facebook">📘</a>
                        <a href="#" title="LinkedIn">💼</a>
                        <a href="#" title="Instagram">📷</a>
                    </div>
                </div>
                
                <div class="footer-section">
                    <h3>Contact Information</h3>
                    <p><strong>Head Office:</strong> Karachi</p>
                    <p><strong>Phone:</strong> +92 21 4312154-5</p>
                    <p><strong>Email:</strong> info@fourcg.com</p>
                    <p><strong>Regional Offices:</strong> Rawalpindi, Lahore</p>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>Copyright © 2025 Four Corners Group Private Limited</p>
            </div>
        </div>
        """
        
        st.markdown(compact_footer_html, unsafe_allow_html=True)