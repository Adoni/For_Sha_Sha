#include	"unp.h"
#include	<string.h>

char buf[MAXLINE];
int client[FD_SETSIZE];
char name[FD_SETSIZE][20];
void Chatroom(int i, int sockfd, ssize_t n)
{    
	int	j;
	char	*pch;
	char	order[MAXLINE];
	char	welcome[100];
	strcpy(order,buf);
	if((pch = strtok(order," "))!=NULL){
		if(strcmp(order,"./nick")==0){		/*change the name*/
			bzero(name[i],20);
			strcpy(name[i],buf+6);
            name[i][strlen(name[i])-1]='\0';
			sprintf(welcome,"%s is in the Room!\n", name[i]);
			printf("%s",welcome);
	for(j=0;j<FD_SETSIZE;j++)
		if(client[j]>0 && j!=i)
			Writen(client[j], welcome ,strlen(welcome)); 
		}
	}

}
int
main(int argc, char **argv)
{
	int		i, maxi, maxfd, listenfd, connfd, sockfd;
	int		nready;
	ssize_t		n;
	fd_set		rset, allset;
	socklen_t	clilen;
	struct sockaddr_in	cliaddr, servaddr;

	listenfd = Socket(AF_INET, SOCK_STREAM, 0);

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family      = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port        = htons(SERV_PORT);

	Bind(listenfd, (SA *) &servaddr, sizeof(servaddr));

	Listen(listenfd, LISTENQ);

	maxfd = listenfd;			/* initialize */
	maxi = -1;					/* index into client[] array */
	for (i = 0; i < FD_SETSIZE; i++){
		client[i] = -1;			/* -1 indicates available entry */
		strcpy(name[i],"Anonaminous");
	}
	FD_ZERO(&allset);
	FD_SET(listenfd, &allset);
/* end fig01 */

/* include fig02 */
	for ( ; ; ) {
		rset = allset;		/* structure assignment */
		nready = Select(maxfd+1, &rset, NULL, NULL, NULL);

		if (FD_ISSET(listenfd, &rset)) {	/* new client connection */
			clilen = sizeof(cliaddr);
			connfd = Accept(listenfd, (SA *) &cliaddr, &clilen);
#ifdef	NOTDEF
			printf("new client: %s, port %d\n",
					Inet_ntop(AF_INET, &cliaddr.sin_addr, 4, NULL),
					ntohs(cliaddr.sin_port));
#endif

			for (i = 0; i < FD_SETSIZE; i++)
				if (client[i] < 0) {
					client[i] = connfd;	/* save descriptor */
					break;
				}
			if (i == FD_SETSIZE)
				err_quit("too many clients");

			FD_SET(connfd, &allset);	/* add new descriptor to set */
			if (connfd > maxfd)
				maxfd = connfd;			/* for select */
			if (i > maxi)
				maxi = i;				/* max index in client[] array */

			if (--nready <= 0)
				continue;				/* no more readable descriptors */
		}

		for (i = 0; i <= maxi; i++) {	/* check all clients for data */
			if ( (sockfd = client[i]) < 0)
				continue;
			if (FD_ISSET(sockfd, &rset)) {
				if ( (n = Read(sockfd, buf, MAXLINE)) == 0) {
						/*4connection closed by client */
					Close(sockfd);
					FD_CLR(sockfd, &allset);
					client[i] = -1;
				} else  
					Chatroom(i,sockfd,n);
//	Chatroom(i,sockfd,n);

				if (--nready <= 0)
					break;				/* no more readable descriptors */
			}
		}
	}
}
