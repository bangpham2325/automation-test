*** Settings ***
Library  SeleniumLibrary
Library  SeleniumLibrary

Default Tags    LTS_STG
*** Variables ***
${url}  https://demo.nopcommerce.com/
${brower}   chrome

*** Test Cases ***

LoginTest (OL-T312531)
   Pass Execution    123

LoginTest (OL-T3125312)
   Pass Execution    123
LoginTest (OL-T3125312)
   Pass Execution    123
LoginTest (OL-T3125312332)
   Pass Execution    123
LoginTest (OL-T31253123332)
    Sleep    100s
   Pass Execution    123
*** Keywords ***
LoginInputText
   click link   xpath://a[contains(text(),'Log in')]
   input text   id:Email    bangpham2501@gmail.com
   input text   id:Password    bangpham2325
   click element    xpath://button[contains(text(),'Log in')]

