Feature: Generic admin functionality

  Background:
    Given "admin" as the persona
    And I log in to the admin interface

  Scenario: View court in new tab
    When I visit "staff/courts"
    Then I should see "Reading Crown Court"
    When I click the link to "/courts/reading-crown-court"
    And I switch to the new window
    Then I should see "Opening hours"
    And I should see "Building facilities"

  Scenario: Find court to edit
    When I visit "staff/courts"
    Then I should see "Reading Crown Court"
    When I click the link to "/staff/court/1"
    Then I should see "Editing - Reading Crown Court"

  Scenario: Add new court
    When I press "add new court"
    And I fill in "name" with "Gotham Crown Court"
    And I press "Add court"
    Then I should see "New court has been added"
    When I view court in the new window
    Then the browser's URL should be "/courts/gotham-crown-court"
    And I should see "This court or tribunal is no longer in service"
