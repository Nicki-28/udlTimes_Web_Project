Feature: Edit Custom Wordle
  In order to modify my custom wordle puzzles
  As a registered user
  I want to edit custom wordles that I created

  Background: There are registered users and a custom wordle
    Given Exists a user "testuser" with password "password123"
    And Exists a user "otheruser" with password "password123"
    And Exists a custom wordle "TEST" created by user "testuser"

  Scenario: Edit custom wordle successfully as the author
    Given I login as user "testuser" with password "password123"
    When I visit the edit page for wordle "TEST"
    And I fill in the word field with "WORDS"
    And I submit the form
    Then I should be on the custom wordle play page

  Scenario: Try to edit custom wordle without being logged in
    Given I am not logged in
    When I visit the edit page for wordle "TEST"
    Then I should be redirected to the login page

  Scenario: Try to edit another user's custom wordle
    Given I login as user "otheruser" with password "password123"
    When I visit the edit page for wordle "TEST"
    Then I should see an access denied message

  Scenario: Edit custom wordle with empty word - validation error
    Given I login as user "testuser" with password "password123"
    When I visit the edit page for wordle "TEST"
    And I fill in the word field with ""
    And I submit the form
    Then I should see an error message about the word