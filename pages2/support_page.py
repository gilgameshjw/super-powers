import streamlit as st

def support_page(config):
    # Support page
    st.title(config.translations["support_title"])
    st.write(config.translations["support_text"])

    # Display bank account details based on language
    if config.language == "en":
        st.text_area("Bank Account Details (English)", config.translations["bank_account_en"])

    elif config.language == "kz":
        st.text_area("Банк шотының деректері (Қазақша)", config.translations["bank_account_kz"])
