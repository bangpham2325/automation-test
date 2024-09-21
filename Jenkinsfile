pipeline {
    agent any

    parameters {
        string(name: 'INSTANCE', defaultValue: 'LTS_STG', description: 'Instance name to be used for testing')
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Get Test Case IDs') {
            steps {
                script {
                    def file = sh(returnStdout: true, script: 'python get_tcs_ids.py').trim()
                    env.file = file
                }
            }
        }

        stage('Run Relevant Tests') {
            steps {
                script {
                    def instance = params.INSTANCE

                    if (env.TCS_IDS) {
                        sh '''pabot --pabotlib --pabotlibport 2999 --testlevelsplit --processes 5 -d results1 -o output.xml --variable env:${INSTANCE} -i ${INSTANCE} -e skip --tagstatinclude ${INSTANCE} $(cat new_tcs.log | tr '\n' ' ') src/'''
                        sh '''pabot --pabotlib --testlevelsplit --processes 5 --rerunfailed results1/output.xml --outputdir results1 --output rerun.xml --variable env:${INSTANCE} -i ${INSTANCE} -e skip --tagstatinclude ${INSTANCE} $(cat new_tcs.log | tr '\n' ' ') src/'''
                        sh "cd results"
                        sh '''rebot --merge --output output.xml --tagstatinclude ${instance} -l log.html -r report.html output.xml rerun.xml'''
                    } else {
                        echo 'No test cases found in this PR'
                    }
                }
            }
        }

        stage('Calculate Pass Percentage') {
            steps {
                script {
                    def totalTests = sh(returnStdout: true, script: "rebot --report none --log none --output none --statistics - | grep 'All Tests' | awk '{print \$3}'").trim()
                    def passedTests = sh(returnStdout: true, script: "rebot --report none --log none --output none --statistics - | grep 'PASSED' | awk '{print \$2}'").trim()

                    if (totalTests.isNumber() && passedTests.isNumber()) {
                        def passPercentage = (passedTests.toDouble() / totalTests.toDouble()) * 100
                        env.PASS_PERCENTAGE = passPercentage.toString()
                        echo "Pass Percentage: ${env.PASS_PERCENTAGE}%"
                    } else {
                        echo "Failed to calculate pass percentage."
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                def passPercentage = env.PASS_PERCENTAGE?.toDouble() ?: 0.0
                if (passPercentage < 5.0) {
                    echo 'Pass percentage is less than 5%, allowing merge...'
                    // Logic to merge PR if needed
                } else {
                    echo 'Pass percentage is greater than or equal to 5%, not allowing merge.'
                    currentBuild.result = 'FAILURE'
                }
            }
        }
        failure {
            echo 'Some relevant tests failed, PR cannot be merged.'
            // Notification or other steps
        }
    }
}
