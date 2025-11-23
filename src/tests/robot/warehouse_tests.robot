*** Settings ***
Documentation     Test suite for Warehouse Manager web application
Library           SeleniumLibrary
Suite Setup       Open Browser To Home Page
Suite Teardown    Close Browser

*** Variables ***
${SERVER}         localhost:5000
${BROWSER}        headlessfirefox
${DELAY}          0
${HOME URL}       http://${SERVER}/

*** Keywords ***
Open Browser To Home Page
    Open Browser    ${HOME URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}

*** Test Cases ***
Home Page Should Load Successfully
    [Documentation]    Verify that the home page loads with the correct title
    Title Should Be    All Warehouses - Warehouse Manager
    Page Should Contain    All Warehouses
    Page Should Contain    Warehouse Manager

Create New Warehouse Successfully
    [Documentation]    Test creating a new warehouse with valid data
    Click Link    xpath=//a[contains(text(), 'Create New Warehouse')]
    Title Should Be    Create Warehouse - Warehouse Manager
    
    Input Text    name=name    Test Warehouse
    Input Text    name=capacity    500
    Input Text    name=initial_stock    100
    
    Click Button    xpath=//button[contains(text(), 'Create Warehouse')]
    
    Title Should Be    All Warehouses - Warehouse Manager
    Page Should Contain    Test Warehouse
    Page Should Contain    100.00
    Page Should Contain    500.00

List All Warehouses
    [Documentation]    Verify that all warehouses are listed on the home page
    Go To    ${HOME URL}
    Page Should Contain    Test Warehouse
    Page Should Contain Element    xpath=//h3[contains(text(), 'Test Warehouse')]

View Warehouse Details
    [Documentation]    Test viewing details of a specific warehouse
    Go To    ${HOME URL}
    Click Link    xpath=//a[contains(text(), 'View Details')]
    
    Page Should Contain    Warehouse Information
    Page Should Contain    Current Stock
    Page Should Contain    Total Capacity
    Page Should Contain    Available Space
    Page Should Contain    Inventory Actions

Add Items To Warehouse
    [Documentation]    Test adding items to a warehouse
    Go To    ${HOME URL}
    Click Link    xpath=//a[contains(text(), 'View Details')]
    
    ${old_stock}=    Get Text    xpath=//span[contains(text(), 'Current Stock')]/following-sibling::span
    
    Input Text    xpath=//h4[contains(text(), 'Add Items')]/following-sibling::form//input[@type='number']    50
    Click Button    xpath=//button[contains(text(), '+ Add')]
    
    Page Should Contain    Warehouse Information
    ${new_stock}=    Get Text    xpath=//span[contains(text(), 'Current Stock')]/following-sibling::span
    Should Not Be Equal    ${old_stock}    ${new_stock}

Remove Items From Warehouse
    [Documentation]    Test removing items from a warehouse
    Go To    ${HOME URL}
    Click Link    xpath=//a[contains(text(), 'View Details')]
    
    ${old_stock}=    Get Text    xpath=//span[contains(text(), 'Current Stock')]/following-sibling::span
    
    Input Text    xpath=//h4[contains(text(), 'Remove Items')]/following-sibling::form//input[@type='number']    25
    Click Button    xpath=//button[contains(text(), '- Remove')]
    
    Page Should Contain    Warehouse Information
    ${new_stock}=    Get Text    xpath=//span[contains(text(), 'Current Stock')]/following-sibling::span
    Should Not Be Equal    ${old_stock}    ${new_stock}

Edit Warehouse
    [Documentation]    Test editing warehouse details
    Go To    ${HOME URL}
    Click Link    xpath=//a[contains(text(), 'View Details')]
    Click Link    xpath=//a[contains(text(), 'Edit')]
    
    Title Should Be    Edit Test Warehouse - Warehouse Manager
    
    Clear Element Text    name=name
    Input Text    name=name    Updated Warehouse Name
    
    Click Button    xpath=//button[contains(text(), 'Save Changes')]
    
    Page Should Contain    Updated Warehouse Name

Toggle Dark And Light Mode
    [Documentation]    Test theme toggle functionality
    Go To    ${HOME URL}
    
    # Check if theme toggle exists
    Page Should Contain Element    xpath=//div[contains(@class, 'theme-toggle')]
    
    # Click theme toggle
    Click Element    xpath=//div[contains(@class, 'theme-toggle')]
    
    # Wait for theme change
    Sleep    0.5s
    
    # Click again to toggle back
    Click Element    xpath=//div[contains(@class, 'theme-toggle')]
    
    # Verify page still works
    Page Should Contain    All Warehouses

Delete Warehouse
    [Documentation]    Test deleting a warehouse
    Go To    ${HOME URL}
    ${warehouse_count_before}=    Get Element Count    xpath=//div[contains(@class, 'warehouse-card')]
    
    Click Link    xpath=//a[contains(text(), 'View Details')]
    
    # Handle the confirmation dialog
    Handle Alert    ACCEPT
    Click Button    xpath=//button[contains(text(), 'Delete Warehouse')]
    
    Title Should Be    All Warehouses - Warehouse Manager
    ${warehouse_count_after}=    Get Element Count    xpath=//div[contains(@class, 'warehouse-card')]
    Should Be True    ${warehouse_count_after} < ${warehouse_count_before}

Create Multiple Warehouses
    [Documentation]    Test creating multiple warehouses to verify grid display
    Go To    ${HOME URL}
    
    # Create first warehouse
    Click Link    xpath=//a[contains(text(), 'Create New Warehouse')]
    Input Text    name=name    Warehouse A
    Input Text    name=capacity    1000
    Input Text    name=initial_stock    200
    Click Button    xpath=//button[contains(text(), 'Create Warehouse')]
    
    # Create second warehouse
    Click Link    xpath=//a[contains(text(), 'Create New Warehouse')]
    Input Text    name=name    Warehouse B
    Input Text    name=capacity    750
    Input Text    name=initial_stock    500
    Click Button    xpath=//button[contains(text(), 'Create Warehouse')]
    
    # Create third warehouse
    Click Link    xpath=//a[contains(text(), 'Create New Warehouse')]
    Input Text    name=name    Warehouse C
    Input Text    name=capacity    2000
    Input Text    name=initial_stock    1500
    Click Button    xpath=//button[contains(text(), 'Create Warehouse')]
    
    # Verify all warehouses are displayed
    Page Should Contain    Warehouse A
    Page Should Contain    Warehouse B
    Page Should Contain    Warehouse C

Cancel Warehouse Creation
    [Documentation]    Test canceling warehouse creation
    Go To    ${HOME URL}
    ${warehouse_count_before}=    Get Element Count    xpath=//div[contains(@class, 'warehouse-card')]
    
    Click Link    xpath=//a[contains(text(), 'Create New Warehouse')]
    Input Text    name=name    Cancelled Warehouse
    
    Click Link    xpath=//a[contains(text(), 'Cancel')]
    
    Title Should Be    All Warehouses - Warehouse Manager
    ${warehouse_count_after}=    Get Element Count    xpath=//div[contains(@class, 'warehouse-card')]
    Should Be Equal As Numbers    ${warehouse_count_before}    ${warehouse_count_after}
    Page Should Not Contain    Cancelled Warehouse
