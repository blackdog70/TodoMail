# TodoMail

Python software to renew email's client philosophy.

## Getting Started

Install dependencies:

```
pip install -r requirements.txt
```

Run the development server:

```
flask --app app:create_app run
```
Visit `http://localhost:5000/register` to create a new account by providing
your first name, last name, email, username, password and preferred language
(English or Italian). After registration you will be redirected to the main
page using the selected language. The language can be changed later from the
navigation bar. Once logged in, open the *Settings* page to add one or more
email server connections, selecting the protocol for receiving mail (IMAP or
POP3). Each connection can be tested with the dedicated button that shows the
result of the check.

## Tests

Run the test suite with:

```
pytest
```
