*** Settings ***
Library  SeleniumLibrary
Library  SeleniumLibrary

Default Tags    LTS_STG
*** Variables ***
${url}  https://demo.nopcommerce.com/
${brower}   chrome

*** Test Cases ***
LoginTest(OL-T1234)
   Pass Execution    123

LoginTest2(OL-T1238)
   Pass Execution    123


LoginTest3(OL-T12349)
   Pass Execution    123


LoginTest4(OL-T12310)
   Pass Execution    123

LoginTest3(OL-T112349)
   Pass Execution    123


LoginTest4(OL-T122310)
   Pass Execution    123


*** Keywords ***
LoginInputText
   click link   xpath://a[contains(text(),'Log in')]
   input text   id:Email    bangpham2501@gmail.com
   input text   id:Password    bangpham2325
   click element    xpath://button[contains(text(),'Log in')]

