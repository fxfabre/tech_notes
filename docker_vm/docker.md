## Docker
-  https://medium.com/@gdiener/how-to-build-a-smaller-docker-image-76779e18d48a
- docker squash : https://blog.codacy.com/five-ways-to-slim-your-docker-images/
- Multi stage build : https://vsupalov.com/build-docker-image-clone-private-repo-ssh-key/

docker basic commands 
- docker pull image_name:tag 
- docker run -p 8080:8080 
- docker logs --follow $docker_id
- docker save my_image | xz > my_image.tar.xz 
- xz -cd my_image.tar.xz | sudo docker load

nettoyer son docker en local et regagner de la place
- docker ps -qa --no-trunc --filter "status=exited"| xargs docker rm
- docker images --filter "dangling=true" -q --no-trunc | xargs docker rmi 
- docker images | grep "none" | awk '/ / { print $3 }' | xargs docker rmi 
- docker volume ls -qf dangling=true | xargs  docker volume rm

## Dockerfile
ADD vs COPY : 
- ADD can use a URL instead of a local file / directory. Secondly, you can extract a tar file from the source directly into the destination.
- If you’re using a URL : you might as well just use RUN with curl instead of ADD so you chain everything into 1 RUN command to make a smaller Docker image.
- If you’re copying in local files to your Docker image, always use COPY because it’s more explicit.

Entrypoint vs CMD
- CMD defines default commands and/or parameters for a container. CMD is an instruction that is best to use if you need a default command which users can easily override.
- ENTRYPOINT is preferred when you want to define a container with a specific executable. You cannot override an ENTRYPOINT when starting a container unless you add the --entrypoint flag.
- Combine ENTRYPOINT with CMD if you need a container with a specified executable and a default parameter that can be modified easily.

Ports vs Expose
- Expose : accessible au réseau du container
- ports : accessible au host en plus

Tips :
- The Docker client sends the entire "build context" to the Docker daemon. That build context (by default) is the entire directory the Dockerfile is in (so, the entire rpms tree). You can setup a .dockerignore file to get Docker to ignore some files.
- Tous les chemins doivent être définis en relatif, à partir du chemin courant (ou chemin donné en dernier parametre au docker build ?). Uniquement les sous dossiers sont accessibles. 

Create a user :
```dockerfile
RUN addgroup --system app && adduser --system --group app \
 && chown -R app:app /app
USER app
```

## Ctop
ctop provides a concise and condensed overview of real-time metrics for multiple containers.
https://github.com/bcicen/ctop

### Docker context
Pour lancer un container sur un remote server via docker-compose
- Creer un context : `docker context create dev_box --description "dev server name" --docker "host=ssh://root@dev-host"`
