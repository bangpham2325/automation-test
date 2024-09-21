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

LoginTest2 (OL-T1233)
   Pass Execution    123

LoginTest (OL-T1239)
   Pass Execution    1235

LoginTest3 (OL-T1239)
   Pass Execution    1235

LoginTest3 (OL-T1269)
   Pass Execution    1235

LoginTest3 (OL-T12619)
   Pass Execution    12352

LoginTest3 (OL-T126219)
   Pass Execution    12352

LoginTest3 (OL-T1262191)
   Pass Execution    12352
*** Keywords ***
LoginInputText
   click link   xpath://a[contains(text(),'Log in')]
   input text   id:Email    bangpham2501@gmail.com
   input text   id:Password    bangpham2325
   click element    xpath://button[contains(text(),'Log in')]

