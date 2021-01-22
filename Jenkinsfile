pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
        stage('Test') {
            steps {
                dir ('lib') {
                    git branch: "master", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                dir ('mysql_lib') {
                    git branch: "master", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/mysql-lib.git"
                }
                dir ('mysql_lib/lib') {
                    git branch: "master", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                sh """
                virtualenv test_env
                source test_env/bin/activate
                pip2 install mock==2.0.0 --user
                pip2 install mysql-connector-python==8.0.16 --user
                ./test/unit/mysql_rep_failover/convert_to_master.py
                ./test/unit/mysql_rep_failover/create_instances.py
                ./test/unit/mysql_rep_failover/gtid_enabled.py
                ./test/unit/mysql_rep_failover/help_message.py
                ./test/unit/mysql_rep_failover/main.py
                ./test/unit/mysql_rep_failover/promote_best_slave.py
                ./test/unit/mysql_rep_failover/order_slaves_on_gtid.py
                ./test/unit/mysql_rep_failover/promote_designated_slave.py
                ./test/unit/mysql_rep_failover/run_program.py
                ./test/unit/mysql_rep_failover/show_best_slave.py
                ./test/unit/mysql_rep_failover/show_slave_delays.py
                deactivate
                rm -rf test_env
                """
            }
        }
        stage('SonarQube analysis') {
            steps {
                sh './test/unit/sonarqube_code_coverage.sh'
                sh 'rm -rf lib'
                sh 'rm -rf mysql_lib'
                script {
                    scannerHome = tool 'sonar-scanner';
                }
                withSonarQubeEnv('Sonar') {
                    sh "${scannerHome}/bin/sonar-scanner -Dproject.settings=sonar-project.JACIDM.properties"
                }
            
            }
        }
        stage('Artifactory upload') {
            steps {
                script {
                    server = Artifactory.server('Artifactory')
                    server.credentialsId = 'art-svc-highpoint-dev'
                    uploadSpec = """{
                        "files": [
                            {
                                "pattern": "./*.py",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mysql-failover/"
                            },
                            {
                                "pattern": "./*.txt",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mysql-failover/"
                            },
                            {
                                "pattern": "./*.md",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mysql-failover/"
                            },
                            {
                                "pattern": "*.TEMPLATE",
                                "recursive": true,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mysql-failover/config/"
                            }
                        ]
                    }"""
                    server.upload(uploadSpec)
                }
            }
        }
    }
}
