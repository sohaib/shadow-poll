/* This suid script is a wrapper to safely (hopefully) run python setuid,
   by cleaning out the environment first.
*/

#ifdef NO_HEADERS
/* Just declare these here, since iphone-gcc doesn't seem to have headers. :( */
void exit(int status);
int execve(const char *path, char *const argv[], char *const envp[]);
#else
#include <unistd.h>
#include <stdlib.h>
#endif

#ifndef PYTHON
#error Makefile should have defined PYTHON
#endif

#ifndef PREFIX
#error Makefile should have defined PREFIX
#endif

#define MAX_ARGS 100

int main(int argc, char **argv)
{
	char *env[] = {"PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin", 0L};
	char *args[MAX_ARGS+2];
	int i;
	args[0] = PYTHON;
	args[1] = PREFIX "/sbin/f5vpn-login.py";
	
	for(i = 1; i < MAX_ARGS && i < argc; i++)
	{
		args[i+1] = argv[i];
	}
	args[i+1] = 0L;
	
	execve(PYTHON, args, env);
	exit(1);
}
