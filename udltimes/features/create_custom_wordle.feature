Feature: Create Custom Wordle
  In order to create custom wordle puzzles for my friends
  As a registered user
  I want to create custom wordles

  Background: There is a registered user
    Given Exists a user "testuser" with password "password123"

  Scenario: Create custom wordle successfully with valid 5-letter word
    Given I login as user "testuser" with password "password123"
    When I visit the wordle creation page
    And I fill in the word field with "CORES"
    And I submit the form
    Then I should be on the custom wordle play page

  Scenario: Try to create custom wordle without being logged in
    Given I am not logged in
    When I visit the wordle creation page
    Then I should be redirected to the login page

  Scenario: Create custom wordle with empty word - validation error
    Given I login as user "testuser" with password "password123"
    When I visit the wordle creation page
    And I fill in the word field with ""
    And I submit the form
    Then I should see an error message about the word

  Scenario: Create custom wordle with invalid length (3 letters)
    Given I login as user "testuser" with password "password123"
    When I visit the wordle creation page
    And I fill in the word field with "SOL"
    And I submit the form
    Then I should see an error message about the word length

  Scenario: Create custom wordle with non-alphabetic characters
    Given I login as user "testuser" with password "password123"
    When I visit the wordle creation page
    And I fill in the word field with "C0R3S"
    And I submit the form
    Then I should see an error message about only letters allowed