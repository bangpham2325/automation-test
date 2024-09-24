*** Settings ***
Library  SeleniumLibrary
Library  SeleniumLibrary

Default Tags    LTS_STG
*** Variables ***
${url}  https://demo.nopcommerce.com/
${brower}   chrome

*** Test Cases ***
LoginTest (OL-T2123)
   Pass Execution    123

LoginTest (OL-T3123)
   Pass Execution    123

LoginTest (OL-T3125)
   Pass Execution    123

LoginTest (OL-T3125)
   Sleep    100s
   Pass Execution    123
LoginTest (OL-T3125)
   Sleep    200s
   Pass Execution    123

LoginTest (OL-T31252323)
   Sleep    200s
   Pass Execution    123
*** Keywords ***
LoginInputText
   click link   xpath://a[contains(text(),'Log in')]
   input text   id:Email    bangpham2501@gmail.com
   input text   id:Password    bangpham2325
   click element    xpath://button[contains(text(),'Log in')]

