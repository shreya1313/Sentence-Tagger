def userInput = true
def didTimeout = false
def scmVariable = null
def gitCommit = null
def commitMessage = null
def ecrUrl = null
def environment = "testing"
def infraRepositoryName = "infra-config-test"


podTemplate(
	label: 'flask-slave',
	containers: [
		containerTemplate(name: 'dind', image: 'spotmentor/dind-git-awscli:1.0.1', privileged: true)
	],
	volumes: [
		hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock'),
	],
) {
	node('flask-slave') {
		stage("Setting Environment") {
			if (env.JOB_NAME.startsWith('prod_')) {
				environment = "production"
				infraRepositoryName = "infra-config-prod"
			}
		}

		stage('Checkout Repository') {
			scmVariable = checkout scm
		}

		// Building docker image
		stage('Building Docker Image') {
			// Getting the information from the SCM variable

			def gitUrl = scmVariable.GIT_URL
			def serviceName = gitUrl.tokenize('/').last().split("\\.")[0]

			gitCommit = scmVariable.GIT_COMMIT.substring(0, 7).trim()
			commitMessage = sh(returnStdout: true, script: "git log -n 1 --pretty=format:%s ${gitCommit}").trim()

			ecrUrl = "${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${serviceName}-testing:${gitCommit}"

			container('dind') {
				sh "docker build -t $serviceName:$gitCommit . && docker tag $serviceName:$gitCommit $ecrUrl"

				def loginCommand = sh(returnStdout: true, script: "aws ecr get-login --region $REGION --no-include-email")

				sh "$loginCommand"

				sh "docker push $ecrUrl"
			}
		}
	}
}


stage('Promotion Stage') {
	try {
		timeout(time: 1, unit: 'DAYS') {
			input("Deploy to ${environment} server?")
		}
	} catch(err) {
		def user = err.getCauses()[0].getUser()

		if ('SYSTEM' == user.toString()) {
			didTimeout = true
		} else {
			userInput = false
		}
		currentBuild.result = 'SUCCESS'
	}
}


if (userInput && !didTimeout) {
	podTemplate(
		label: 'flask-slave',
		containers: [
			containerTemplate(name: 'dind', image: 'spotmentor/dind-git-awscli:1.0.1', privileged: true)
		],
	) {
		node('flask-slave') {
			container('dind') {
				def credentialId = sh(returnStdout: true, script: "echo ${CREDENTIALS_ID}")

				gitUrl = scmVariable.GIT_URL
				serviceName = gitUrl.tokenize('/').last().split("\\.")[0]

				withCredentials([[
					$class: 'UsernamePasswordMultiBinding', credentialsId: credentialId,
					usernameVariable: 'BITBUCKET_USERNAME', passwordVariable: 'BITBUCKET_PASSWORD'
				]]) {
					// Clone the infra repository
					sh "git config credential.helper 'cache --timeout=300'"

					stage('Perform repo update or clone') {
						if (fileExists(infraRepositoryName)) {
							dir(infraRepositoryName) {
								sh(returnStatus: true, script: "git pull --rebase")
							}
						}
						else {
							sh(returnStatus: true, script: "git clone https://${BITBUCKET_USERNAME}:${BITBUCKET_PASSWORD}@bitbucket.org/spotinfra/${infraRepositoryName}.git")
						}
					}

					stage('Update infrastructure codebase') {

						dir(infraRepositoryName) {
							sh "python update_deployment_spec.py --service ${serviceName} --image_url ${ecrUrl} --commit_hash ${gitCommit} --commit_message '${commitMessage}' --environment ${environment}"

							sh "git config user.email 'arpitgoyal.thunderbird@gmail.com' && git config user.name 'Jenkins Slave'"

							sh(returnStatus: true, script:"git add -A && git commit -m 'updated ${serviceName} deployment file for service commit hash - ${gitCommit}' && git push origin master")
						}
					}
				}
			}
		}
	}
}
