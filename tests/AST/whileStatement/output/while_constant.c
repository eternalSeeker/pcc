FileAST: 
  Decl: foo, [], [], []
    FuncDecl: 
      ParamList: 
        Typename: None, []
          TypeDecl: None, []
            IdentifierType: ['void']
      TypeDecl: foo, []
        IdentifierType: ['void']
  FuncDef: 
    Decl: foo, [], [], []
      FuncDecl: 
        ParamList: 
          Typename: None, []
            TypeDecl: None, []
              IdentifierType: ['void']
        TypeDecl: foo, []
          IdentifierType: ['void']
    Compound: 
      Decl: i, [], [], []
        TypeDecl: i, []
          IdentifierType: ['int']
        Constant: int, 10
      While: 
        Constant: int, 0
        Compound: 
          Assignment: =
            ID: i
            BinaryOp: -
              ID: i
              Constant: int, 1
