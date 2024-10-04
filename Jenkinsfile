pipeline {
    agent any

    parameters {
        string(
            name: 'INSTANCE',
            defaultValue: 'LTS_STG',
            description: 'Instance name to be used for testing'
        )
        string(
            name: 'ACCOUNT_NAME',
            defaultValue: 'bangpham2325',
            description: 'GitHub account that owns the repos that contains the commit to notify'
        )
        string(
            name: 'GITHUB_API_URL',
            defaultValue: 'https://github.com/bangpham2325/automation-test.git'
        )
        credentials(
            name: 'CREDENTIALS_ID',
            defaultValue: '123123',
            description: 'The GitHub credentials, username/password or username/accessToken'
        )
    }
    environment {
        // Define the python_path dynamically based on the job name and environment
        python_path = "/var/lib/jenkins/workspace/"
        GITHUB_API_URL="${params.GITHUB_API_URL}"
        credentialsId = "${params.CREDENTIALS_ID}"
        account="${params.ACCOUNT_NAME}"
    }
    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
                script {
                    // Get the latest commit SHA and save it in an environment variable
                    env.GIT_COMMIT = sh(script: "git rev-parse HEAD", returnStdout: true).trim()
                    echo "Latest commit SHA: ${env.GIT_COMMIT}"
                }
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
                    def result = sh(
                        script: '''
                            set +e
                            # Activate the virtual environment
                            . venv/bin/activate
                            pip install GitPython
                            # You can now run Python commands or scripts here
                            python --version
                            python get_tcs_ids.py
                            python_path="/var/lib/jenkins/workspace/"$JOB_NAME$ENV
                            export PYTHONPATH=$python_path
                            # Check if new_tcs.log has data
                            if [ -s new_tcs.log ]; then
                                echo "new_tcs.log has data, proceeding with tests..."
                                pabot --pabotlib --pabotlibport 2999 --testlevelsplit --processes 5 -d results -o output.xml --variable env:${INSTANCE} -i ${INSTANCE} -e skip --tagstatinclude ${INSTANCE} $(cat new_tcs.log | tr '\n' ' ') src/tests_suites
                                echo "hello"
                                pabot --pabotlib --testlevelsplit --processes 5 --rerunfailed results/output.xml --outputdir results --output rerun.xml --variable env:${INSTANCE} -i ${INSTANCE} -e skip --tagstatinclude ${INSTANCE} src/tests_suites
                                cd results
                                rebot --merge --output output.xml --tagstatinclude ${INSTANCE} -l log.html -r report.html output.xml rerun.xml
                                exit 0
                            else
                                echo "new_tcs.log is empty, skipping tests."
                                exit 1
                            fi
                            set -e
                        ''', returnStatus: true
                    )

                    if (result == 1) {
                        env.LIST_TCS = 'False'
                        echo "LIST_TCS is set to False"
                    } else {
                        env.LIST_TCS = 'True'
                        echo "LIST_TCS is set to True"
                    }
                }
            }
        }

        stage('Calculate Pass Percentage') {
            steps {
                script {
                    if (env.LIST_TCS == 'False') {
                        echo 'Skipping pass percentage calculation as there are no tests to run.'
                        env.PASS_PERCENTAGE = 100
                        return
                    }
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
                    githubNotify account: "${env.account}", context: 'Jenkins', credentialsId: "${env.credentialsId}", description: "Pass percentage is greater than 90%, allowing merge.", gitApiUrl: '', repo: 'automation-test', sha: "${env.GIT_COMMIT}", status: 'SUCCESS', targetUrl: "${env.BUILD_URL}"
                } else {
                    echo 'Pass percentage is less than or equal to 90%, not allowing merge.'
                    githubNotify account: "${env.account}", context: 'Jenkins', credentialsId: "${env.credentialsId}", description: "Pass percentage is less than or equal to 90%, not allowing merge.", gitApiUrl: '', repo: 'automation-test', sha: "${env.GIT_COMMIT}", status: 'FAILURE', targetUrl: "${env.BUILD_URL}"
                }
            }
        }
        always {
            cleanWs()
        }
        failure {
            echo 'Some relevant tests failed, PR cannot be merged.'
            githubNotify account: "${env.account}", context: 'Jenkins', credentialsId: "${env.credentialsId}", description: "Some relevant tests failed, PR cannot be merged.", gitApiUrl: '', repo: 'automation-test', status: 'FAILURE',sha: "${env.GIT_COMMIT}", targetUrl: "${env.BUILD_URL}"
        }
    }
}