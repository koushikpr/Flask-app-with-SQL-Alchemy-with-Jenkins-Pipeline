// TO help jenkins get the path right -> add PATH="$HOME/.local/bin:$PATH" at end of the file /etc/profile and restart the jenkins.

pipeline {
    agent {
        label 'local'
    }
    environment {
        // This is my EC2 Server Public Address
        dev_app_server = "192.168.0.112"
        dev_app_user = "ubuntu"
    }
    options {
        timestamps()
        ansiColor('xterm')
        timeout(time: 5, unit: 'MINUTES')
    }
    stages {
        stage('Building') {
            options {
                timeout(time: 1, unit: "MINUTES")
            }
            steps {
                echo 'Starting build'
                sh '''
                    sudo apt -y install python3.9
                    sudo apt -y install python3-pip
                    pip3 install --upgrade pip
                    pip3 install virtualenv
                    virtualenv -p /usr/bin/python3.9 venv
                    . venv/bin/activate
                    pip3 install -r requirements.txt
                '''
                echo 'Building Success'
            }
        }
        stage('Linting and Testing') {
            steps {
                parallel(
                    a: {
                        echo 'Starting lint'
                        sh '''
                        . venv/bin/activate
                        pylint --output-format=parseable --fail-under=95 app/app.py --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" | tee pylint.log || echo "pylint exited with $?"
                        '''
                        echo "Linting Success"
                    },
                    b: {
                        echo 'Starting test'
                        sh '''
                        . venv/bin/activate
                        pytest --cov=tests --cov-report term -vs
                        '''
                        echo "Testing Success"
                    }
                )
                }
        }
        stage('Deploy') {
            steps {
                echo 'Starting deploy to the app server'
                sh '''
                . venv/bin/activate
                ssh  ${dev_app_user}@${dev_app_server} "mkdir -p /home/${dev_app_user}/webapp"
                rm -rf venv
                echo "Env is"
                echo "${WORKSPACE}"
                echo "Env done"
                scp -pr "${WORKSPACE}"/*  ${dev_app_user}@${dev_app_server}:/home/${dev_app_user}/webapp/
                ssh  ${dev_app_user}@${dev_app_server} "cd /home/${dev_app_user}/webapp/; . /home/${dev_app_user}/.bashrc; . ./deploy.sh"
                '''
                echo "Deployment Success"
            }
        }
    }
}