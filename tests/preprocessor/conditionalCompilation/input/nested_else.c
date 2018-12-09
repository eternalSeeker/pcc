int start;
#define YES
#define YES_NO
#ifdef YES
    #ifdef YES_YES
        void yes(void);
    #else
        void yes_no(void);
        int this_is_it;
    #endif
#else
    #ifdef YES_YES
        void no_yes(void);
        int no;
    #else
        void no_no(void);
    #endif
#endif
int end;
