*** Settings ***
Library  SeleniumLibrary
Library  SeleniumLibrary

Default Tags    LTS_STG
*** Variables ***
${url}  https://demo.nopcommerce.com/
${brower}   chrome

*** Test Cases ***
LoginTest (OL-T123)
   Pass Execution    123

LoginTest (OL-T1235, OL-T1236)
   Pass Execution    123
LoginTest (OL-T1237,22OL-T1238)
   Pass Execution    123
LoginTest (OL-T1237,OL-T1238)
   Pass Execution    123
   # tcs (OL-T1238)
*** Keywords ***
LoginInputText
   click link   xpath://a[contains(text(),'Log in')]
   input text   id:Email    bangpham2501@gmail.com
   input text   id:Password    bangpham2325
   click element    xpath://button[contains(text(),'Log in')]

