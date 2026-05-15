Feature: Delete Custom Wordle
  In order to remove custom wordle puzzles I no longer want
  As a registered user
  I want to delete custom wordles that I created

  Background: There are registered users and a custom wordle
    Given Exists a user "testuser" with password "password123"
    And Exists a user "otheruser" with password "password123"
    And Exists a custom wordle "DELETE" created by user "testuser"

  Scenario: Delete custom wordle successfully as the author
    Given I login as user "testuser" with password "password123"
    When I visit the delete page for wordle "DELETE"
    And I click the delete button
    Then I should be on the home page
    And The wordle "DELETE" should not exist

  Scenario: Try to delete custom wordle without being logged in
    Given I am not logged in
    When I visit the delete page for wordle "DELETE"
    Then I should be redirected to the login page

  Scenario: Try to delete another user's custom wordle
    Given I login as user "otheruser" with password "password123"
    When I visit the delete page for wordle "DELETE"
    Then I should see an access denied message