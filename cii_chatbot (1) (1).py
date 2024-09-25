# Import necessary libraries
import requests  # To make HTTP requests
from bs4 import BeautifulSoup  # To parse HTML content
import streamlit as st  # For building the Streamlit web app
from nltk.corpus import stopwords  # To remove common stopwords from text
from nltk.tokenize import word_tokenize  # To break text into individual words (tokens)

# Function to scrape a CII press release from a given URL
def scrape_cii_press_release(url):
    try:
        # Send an HTTP request to the provided URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request fails

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the press release title, summary, and publication date
        title = soup.find('h1', class_='press-release-title').text
        summary = soup.find('p', class_='summary').text
        date = soup.find('time').text

        # Return the extracted data as a dictionary
        return {'title': title, 'summary': summary, 'date': date}
    except Exception as e:
        # Print an error message if something goes wrong during scraping
        print(f"Error scraping {url}: {e}")
        return None

# Function to scrape multiple press releases from a list of URLs
def scrape_multiple_press_releases(urls):
    data = []  # List to store the press release data
    for url in urls:
        # Scrape each press release and add the data to the list
        press_release_data = scrape_cii_press_release(url)
        if press_release_data:
            data.append(press_release_data)
    return data

# Function to answer user questions by comparing them to press release summaries
def answer_question(question, data):
    # Tokenize and remove stopwords from the user's question
    question_words = set(word_tokenize(question.lower())) - set(stopwords.words('english'))
    for item in data:
        # Tokenize and remove stopwords from the press release summaries
        item_words = set(word_tokenize(item['summary'].lower())) - set(stopwords.words('english'))
        # If there is a significant overlap between the question and summary, return the relevant press release
        if len(question_words.intersection(item_words)) / len(question_words) > 0.5:
            return item
    return "I couldn't find any relevant information for your question."

# Main function to run the Streamlit app
def main():
    st.title("CII Press Release Chatbot")  # Set the title of the web app

    # Input field for the user's question
    user_question = st.text_input("Ask a question about CII press releases:")

    # When the 'Submit' button is pressed
    if st.button("Submit"):
        # List of CII press release URLs to scrape
        urls = [
            "https://www.cii.in/PolicyAdvocacyDetails.aspx?enc=82IhkgLstN7uRV+oMxFElgyDQvwT5K+kp2BNevnf8jKU6QKNVruuchLYc/ZX0nJ/IgmTZ1oGDPxzVgsNyM+x7XdpbqVgUSa6ZTdN3O4T5Kf6xrnHDC+NuhJ9phVQApSpvYXp6/Vj5Qd9eKL+eldZcyHiqy4o8+cFK+Wfk4/nNkyB9TgGw6ohhCBcs987VfaqthdGGAu8MoTWOwAixou1nA==",
            "https://www.cii.in/PolicyAdvocacyDetails.aspx?enc=SGS2mHHaiYJIXjG5zJOcOIDp7NClNwIDjUqATVUMmmDqTP6UnQgyHVi3rwDFmBBXpyUA68YuShrfxqqC39xqWsihAEhTwlCOk1P+X0/Bwa8tS8AHp8nrPAL/709d0iLuSbIC2JWtHpEJ7riKloPMiRtXGJgY2UUOSqUNcjYBn6ScTsJwPt91zfQLbxxMqWERwR/U7alAxZuwIG9RCslneg=="
        ]

        # Scrape the data from the provided URLs
        data = scrape_multiple_press_releases(urls)

        # Get a response based on the user's question
        response = answer_question(user_question, data)

        # Display the response in a text area
        st.text_area("Response", value=response)

# Entry point of the script
if __name__ == "__main__":
    main()
