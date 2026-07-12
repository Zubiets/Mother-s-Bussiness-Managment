## Description
- Useful tool to catch error prior the user. This library has a lot of good functions to help us in the tests and make the commands easier
## Tools used
- assert: A so useful tool to identify logical errors, verify a condition made by the programmer and if that conditions failed is printed a error message.
- Fixture: Decorator that makes function test callable in the arguments of other tests to avoid repetition. Prior of every test function, will be execute the fixture.
- Yield: return a specific element of the fixture function (The database), making sure that although something failed during the tests, the next line of code will be executed (The database's close)
## Links
- https://docs.pytest.org/en/stable/search.html?q=-v+&check_keywords=yes&area=default