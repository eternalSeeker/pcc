FileAST: 
  Decl: foo, [], [], []
    FuncDecl: 
      ParamList: 
        Typename: None, []
          TypeDecl: None, []
            IdentifierType: ['void']
      TypeDecl: foo, []
        IdentifierType: ['int']
  FuncDef: 
    Decl: foo, [], [], []
      FuncDecl: 
        ParamList: 
          Typename: None, []
            TypeDecl: None, []
              IdentifierType: ['void']
        TypeDecl: foo, []
          IdentifierType: ['int']
    Compound: 
      Decl: i, [], [], []
        TypeDecl: i, []
          IdentifierType: ['int']
        Constant: int, 0
      If: 
        ID: i
        Compound: 
          Assignment: =
            ID: i
            Constant: int, 5
      Return: 
        ID: i
