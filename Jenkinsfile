pipeline {
    agent {
        node {
            label 'jenkins-agent-docker'
        }
    }

    // // утилиты которые можно объявить и далее использовать
    // tools {

    //     // утилита должна быть установлена и настроена через UI Jenkins 
    //     maven 'Maven'
    // }

    // // параметры которые можно определить и далее использовать
    // parameters {

    //     // сначала указывается тип параметра
    //     string(name: 'SERVICE', defaultValue: 'todo-backend', description: 'service name')
    //     choice(name: 'VERSION', choices: ['1.0.0', '2.0.0', '3.0.0'], description: 'version to deploy on prod')
    //     booleanParam(name: 'executeTests', defaultValue: true, description: '')
    // }

    // // все переменные для docker-контейнера можно определить через UI Jenkins 
    // // Manage Jenkins -> Clouds -> Docker Agent templates -> Countainer settings -> Environment
    // environment {

    //     GIT_REPOSITORY=''
    //     GIT_BRANCH_NAME='main'
    //     GIT_CREDENTIALS='GIT_CREDENTIALS'

    //     DOCKER_REGISTRY='https://hub.docker.com'
    //     DOCKER_REPOSITORY=''

    //     // // функция credentials() - находится в плагине Credentials Binding, получает из хранилища Jenkins (плагин Credentials) креды по id
    //     // DOCKER_CREDENTIALS=credentials('DOCKER_CREDENTIALS')

    //     // просто объявление id кред от DockerHub
    //     DOCKER_CREDENTIALS='DOCKER_CREDENTIALS'

    //     SERVICE_NAME='todo-backend'
    //     VERSION='0.1.0'
    // }

    // // каждые 5 минут jenkins будет проверять git-репозиторий на появление новых коммитов
    // // если будет найден новый коммит, будет запущен build job-ы
    // triggers {
    //     poolSCM 'H/5 * * * *'
    // }

    stages {

        // stage('Clone') {
        //     steps {
        //         echo 'Clone...'

        //         // git url: env.GIT_REPOSITORY
        //         // git url: env.GIT_REPOSITORY, branch: env.GIT_BRANCH_NAME
        //         git url: env.GIT_REPOSITORY, branch: env.GIT_BRANCH_NAME, credentialsId: env.GIT_CREDENTIALS
        //     }
        // }

        stage('Build') {

            steps {

                // двойные кавачки чтобы вставить переменную
                echo "Build ${SERVICE_NAME} on ${VERSION} version..."

                // внутри блока script можно записывать groovy код
                script {
                    dockerImage = docker.build("${DOCKER_REPOSITORY}:${VERSION}")
                }

                // // более понятный код
                // sh "docker build -t ${SERVICE_NAME}:${VERSION} ."

                // sh "docker tag ${SERVICE_NAME}:${VERSION} ${DOCKER_REPOSITORY}:${VERSION}"

                // sh "docker build -t ${DOCKER_REPOSITORY}:${VERSION} ."
            }
        }

        stage('Test') {

            // условие при котором шаг будет выполняться
            when {

                // // условие из параметров
                // // if True: ...
                // expression {
                //     params.executeTests
                // }

                expression {

                    // BRANCH_NAME - стандартная переменная окружения
                    // || - OR
                    // && - AND
                    // /env-vars.html/ - все стандартные переменные окружения
                    env.BRANCH_NAME == 'dev' || env.BRANCH_NAME == 'staging'
                }
            }

            steps {
                
                echo 'Test...'
            }
        }

        stage('Push') {

            steps {

                echo 'Push...'

                script {
                    docker.withRegistry('', DOCKER_CREDENTIALS) {
                        dockerImage.push()
                    }
                }

                // // более понятный код
                // echo 'Login...'

                // // // использование переменных полученных в credentials() внутри environment
                // // sh "docker login -u $DOCKER_CREDENTIALS_USR -p $DOCKER_CREDENTIALS_PSW $DOCKER_REGISTRY"

                // // // withCredentials() - позволяет использовать креды из хранилища Jenkins только в данном месте, без необходимости записывать их в переменную в environment
                // // // usernamePassword() - получение сохранённых в хранилище Jenkins кред по credentialsId, в данном случае - 'DOCKER_CREDENTIALS'
                // // // запись логина и пароля в переменные переданные в usernameVariable и passwordVariable
                // // withCredentials([usernamePassword(credentialsId: 'DOCKER_CREDENTIALS', usernameVariable: 'DOCKER_LOGIN', passwordVariable: 'DOCKER_PASSWORD')]) {

                // //     // использование переменных полученных в usernamePassword()
                // //     sh "docker login -u $DOCKER_LOGIN -p $DOCKER_PASSWORD $DOCKER_REGISTRY"
                // // }

                // // использование переменных полученных в credentials() внутри environment
                // // docker просит использовать --password-stdin
                // sh "echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin $DOCKER_REGISTRY"

                // echo 'Push...'
                // sh "docker push ${DOCKER_REPOSITORY}:${VERSION}"

                // echo 'Logout...'
                // sh 'docker logout'
            }
        }

        stage('Remove') {
            steps {
                echo 'Remove...'

                sh "docker rmi ${DOCKER_REPOSITORY}:${VERSION}"
            }
        }
    }

    // // действие после всех шагов
    // post {

    //     // выполнится независимо от того упал билд или нет
    //     always {
    //         cleanWs(deleteDirs: true, disableDeferredWipeout: true, notFailBuild: true)
    //     }

    //     // выполнится только если билд завершился успешно
    //     success {

    //     }

    //     // выполнится только если билд упал
    //     faiure {

    //     }
    // }
}