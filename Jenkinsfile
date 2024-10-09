pipeline {
    agent any

    environment {
        // Define the python_path dynamically based on the job name and environment
        python_path = "/var/lib/jenkins/workspace/"
        GITHUB_API_URL="https://github.com/bangpham2325/automation-test.git"
        credentialsId = "123123"
        account="bangpham2325"
        instance = "LTS_STG"
    }
    stages {
        stage('Checkout PR') {
            steps {
                script {
                    // Fetch the pull request
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: "pr/${ghprbPullId}/head"]],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [],
                        userRemoteConfigs: [[url: "${env.GITHUB_API_URL}"]]
                    ])

                    // Get branch name
                    def branchName = "${ghprbSourceBranch}"
                    echo "Branch name: ${branchName}"
                    // Check if the branch starts with 'implement/'
                    if (branchName.contains("implement/")) {
                        echo "Branch ${branchName} starts with 'implement/'. Proceeding with the build."
                    } else {
                        echo "Branch ${branchName} does not start with 'implement/'. This PR does not require further testing."
                        currentBuild.result = 'SUCCESS'  // Set the build result as SUCCESS
                        error("Stopping the job as the branch does not start with 'implement/'.")  // Stop the job
                    }
                }
            }
        }
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
                                results_dir="results_${BUILD_NUMBER}"
                                mkdir -p ${results_dir}
                                echo "new_tcs.log has data, proceeding with tests..."
                                pabot --pabotlib --testlevelsplit --processes 5 -d ${results_dir} -o output.xml --variable env:${instance} -i ${instance} -e skip --tagstatinclude ${instance} $(cat new_tcs.log | tr '\n' ' ') src/tests_suites
                                echo "hello"
                                pabot --pabotlib --testlevelsplit --processes 5 --rerunfailed ${results_dir}/output.xml --outputdir ${results_dir} --output rerun.xml --variable env:${instance} -i ${instance} -e skip --tagstatinclude ${instance} src/tests_suites

                                cd ${results_dir}
                                rebot --merge --output output.xml --tagstatinclude ${instance} -l log.html -r report.html output.xml rerun.xml
                                echo "${results_dir}" > ../results_dir.txt
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
                        env.RESULTS_DIR = readFile('results_dir.txt').trim()
                        echo "LIST_TCS is set to True"
                        echo "RESULTS_DIR is set to ${env.RESULTS_DIR}"
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
                    def resultsDir = env.RESULTS_DIR ?: "results_${BUILD_NUMBER}"
                    if (!env.RESULTS_DIR) {
                        echo "RESULTS_DIR not set. Using default: ${resultsDir}"
                    }
                    def passPercentage = sh(script: "python3 ${pythonScriptPath} ${resultsDir}", returnStdout: true).trim()

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
        failure {
            echo 'Some relevant tests failed, PR cannot be merged.'
            githubNotify account: "${env.account}", context: 'Jenkins', credentialsId: "${env.credentialsId}", description: "the job as the branch does not start with 'implement/'", gitApiUrl: '', repo: 'automation-test', status: 'FAILURE', sha: "${env.GIT_COMMIT}", targetUrl: "${env.BUILD_URL}"
        }
    }
}