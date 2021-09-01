// need to edit

def VERSION_NUMBER
def BUILD_DATE = new Date().format("yyyyMMdd")
def BUILD_NUMBER = env.BUILD_NUMBER

pipeline {
    agent any
    environment {
        DEV_SERVER_IP = credentials("Dev_Server_IP")
	    HARBOR_IP = credentials("harbor_ip")
        HARBOR_PROJECT_NAME = "send_ip_for_me"
        SERVER_CONTAINER_NAME = "send_ip_for_me"
        IMAGE_NAME = "send_ip_for_me"
	GPG_PASSPHRASE = credentials("gpg-passphrase")
    }
    stages {
        stage("Test") {
            steps {
                echo "******************"
                echo "hello jenkins test"
                echo "******************"
            }
        }
        stage("Generate Master Version Number") {
            when {
                expression {
                    env.GIT_BRANCH == "gitea/master"
                }
            }
            steps {
                script {
                   VERSION_NUMBER = "v." + BUILD_DATE + "_dev_" + BUILD_NUMBER
                }
                echo "Version Number: $VERSION_NUMBER"
            }
        }
        stage('Setting .env For Stage Server and build image') {
            when {
                expression {
                    env.GIT_BRANCH == "origin/master"
                }
            }
            steps {
                sh "ls -al"
                // rename file so that we don't need to edit the .env name
                sh "echo 'BACKEND_VERSION_NUMBER=$VERSION_NUMBER' >> .env"
                sh "cat .env"
                sh "docker build -t $HARBOR_IP/$HARBOR_PROJECT_NAME/$IMAGE_NAME:${VERSION_NUMBER} ."
            }
        }

        stage("Login Registry & Push Image") {
	    when {
                expression {
                    env.GIT_BRANCH == "origin/develop" || env.GIT_BRANCH == "origin/master"
                }
            }
            steps {
                withCredentials([usernamePassword(
                                    credentialsId: "jenkins_in_harbor",
                                    usernameVariable: "USERNAME",
                                    passwordVariable: "PASSWORD")]) {
                    sh "docker login $HARBOR_IP -u $USERNAME -p $PASSWORD"
                    sh "docker push $HARBOR_IP/$HARBOR_PROJECT_NAME/$IMAGE_NAME:${VERSION_NUMBER}"
                }
            }
        }

        stage("Deploy on Stage Server") {
	    when {
                expression {
                    env.GIT_BRANCH == "origin/master"
                }
            }
            steps {
                withCredentials([usernamePassword(
                                    credentialsId: "stage_server_in_harbor",
                                    usernameVariable: "USERNAME",
                                    passwordVariable: "PASSWORD")]) {
                    sh """
                        docker login $HARBOR_IP -u $USERNAME -p $PASSWORD
                        ls
                        pwd
                        docker rm -f $SERVER_CONTAINER_NAME

                        docker run -d -p 53001:80 --rm -v /home/roykuo/docker_log/send_ip_for_me:/Send_IP_for_me/logs --name $SERVER_CONTAINER_NAME --network bridge $HARBOR_IP/$HARBOR_PROJECT_NAME/$SERVER_CONTAINER_NAME:${VERSION_NUMBER}
                        docker exec -itd $SERVER_CONTAINER_NAME python manage.py
                        exit
                    EOF"""
                }
            }
        }
    }
    post {
        always {
            cleanWs()
            dir("${env.WORKSPACE}@tmp") {
                deleteDir()
            }
            dir("${env.WORKSPACE}@script") {
                deleteDir()
            }
            dir("${env.WORKSPACE}@script@tmp") {
                deleteDir()
            }
            dir("${env.WORKSPACE}@2") {
                deleteDir()
            }
	    dir("${env.WORKSPACE}@2@tmp") {
                deleteDir()
            }
        }
    }
}