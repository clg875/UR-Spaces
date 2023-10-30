CREATE TABLE [dbo].[Moderater] (
  [User_ID] [int] IDENTITY,
  [Special_P] [bit] NULL,
  CONSTRAINT [PK_Moderater] PRIMARY KEY CLUSTERED ([User_ID])
)
ON [PRIMARY]
GO

ALTER TABLE [dbo].[Moderater]
  ADD CONSTRAINT [FK_Moderater_User] FOREIGN KEY ([User_ID]) REFERENCES [dbo].[User] ([User_ID])
GO