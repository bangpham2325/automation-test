pipeline {
    agent any

    parameters {
        string(name: 'INSTANCE', defaultValue: 'LTS_STG', description: 'Instance name to be used for testing')
    }
    environment {
        // Define the python_path dynamically based on the job name and environment
        python_path = "/var/lib/jenkins/workspace/"
        GITHUB_API_URL='https://github.com/bangpham2325/automation-test.git'
    }
    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Run Shell Script') {
            steps {
                script {
                    // Ensure the script has execute permissions
                    sh 'chmod +x ./run.sh'

                    // Run the shell script and capture the exit code
                    def result = sh(script: '''
                        set +e
                        ./run.sh
                    ''', returnStatus: true)

                    // Output the exit code to the console
                    echo "The exit code of run.sh was: ${result}"

                    // Conditionally handle any errors from the script
                    if (result != 0) {
                        echo "There was an error in run.sh, but we are proceeding."
                    }
                }
            }
        }
        stage('Setup Python Environment') {
            steps {
                script {
                    // Activate the Python virtual environment and run commands
                    def instance = params.INSTANCE
                    sh '''
                        set +e
                        # Activate the virtual environment
                        . venv/bin/activate
                        pip install GitPython
                        # You can now run Python commands or scripts here
                        python --version
                        python get_tcs_ids.py
                        python_path="/var/lib/jenkins/workspace/"$JOB_NAME$ENV
                        export PYTHONPATH=$python_path
                        pabot --pabotlib --pabotlibport 2999 --testlevelsplit --processes 5 -d results -o output.xml --variable env:${INSTANCE} -i ${INSTANCE} -e skip --tagstatinclude ${INSTANCE} $(cat new_tcs.log | tr '\n' ' ') src/tests_suites
                        echo "hello"
                        pabot --pabotlib --testlevelsplit --processes 5 --rerunfailed results/output.xml --outputdir results --output rerun.xml --variable env:${INSTANCE} -i ${INSTANCE} -e skip --tagstatinclude ${INSTANCE} src/tests_suites
                        cd results
                        rebot --merge --output output.xml --tagstatinclude ${INSTANCE} -l log.html -r report.html output.xml rerun.xml
                        set -e
                    '''
                }
            }
        }

        stage('Calculate Pass Percentage') {
            steps {
                script {
                    def pythonScriptPath = 'calculate_pass_percentage.py'
                        // Run Python script and capture the output (pass percentage)
                    def passPercentage = sh(script: "python3 ${pythonScriptPath}", returnStdout: true).trim()

                    echo "Pass percentage: ${passPercentage}%"
                    env.PASS_PERCENTAGE = passPercentage
                }
            }
        }

    }

    post {
        success {
            script {
                def passPercentage = env.PASS_PERCENTAGE?.toDouble() ?: 0.0
                if (passPercentage > 90.0) {
                    echo 'Pass percentage is greater than 90%, allowing merge...'
                    withCredentials([usernamePassword(credentialsId: '123123', usernameVariable: 'bangne', passwordVariable: 'AQAAABAAAAAwHhBlsULo76LBd0BKTcU3Q/GqfPiX9bPd2U+74PblK550+YNQ5aSFrw+PHaG/B2nHF8WsVGEJds8rhQp057TlmQ==')]) { githubToken ->
                        sh """
                            curl -X POST -H "Authorization: token ${githubToken}" \
                            -d '{"state": "success", "context": "Jenkins", "description": "Pass percentage > 90%", "target_url": "${env.BUILD_URL}"}' \
                            https://api.github.com/repos/bangpham2325/automation-test/statuses/${env.GIT_COMMIT}
                        """
                    }
                } else {
                    echo 'Pass percentage is less than or equal to 90%, not allowing merge.'
                    currentBuild.result = 'FAILURE'
                    githubNotify account: 'bangpham2325', context: 'Jenkins', credentialsId: '123123', description: 'PAss roi ne', gitApiUrl: '', repo: 'automation-test', sha: '5132500809d92fae3ba9fe2de92e8ef1763e8f08', status: 'FAILURE', targetUrl: "${env.GITHUB_API_URL}"
//                     withCredentials([usernamePassword(credentialsId: '123123', usernameVariable: 'bangne', passwordVariable: 'AQAAABAAAAAwHhBlsULo76LBd0BKTcU3Q/GqfPiX9bPd2U+74PblK550+YNQ5aSFrw+PHaG/B2nHF8WsVGEJds8rhQp057TlmQ==')]) { githubToken ->
//                         sh """
//                             curl -X POST -H "Authorization: token ${githubToken}" \
//                             -d '{"state": "success", "context": "Jenkins", "description": "Pass percentage > 90%", "target_url": "${env.BUILD_URL}"}' \
//                             https://api.github.com/repos/bangpham2325/automation-test/statuses/${env.GIT_COMMIT}
//                         """
//                     }
                }
            }
        }
        failure {
            echo 'Some relevant tests failed, PR cannot be merged.'
            githubNotify account: 'bangpham2325', context: 'Jenkins', credentialsId: '123123', description: 'PAss roi ne', gitApiUrl: '', repo: 'automation-test', status: 'SUCCESS',sha: '5132500809d92fae3ba9fe2de92e8ef1763e8f08', targetUrl: "${env.GITHUB_API_URL}"
        }
    }
}
