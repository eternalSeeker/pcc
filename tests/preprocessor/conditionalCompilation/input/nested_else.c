#define YES
#define YES_NO
#ifdef YES
#ifdef YES_YES
void yes(void);
#else
void yes_no(void);
#endif
#else
#ifdef YES_YES
void no_yes(void);
#else
void no_no(void);
#endif
#endif