CREATE TABLE [dbo].[Student] (
  [User_ID] [int] IDENTITY,
  [Bio] [nvarchar](max) NULL,
  [Banned] [bit] NULL,
  [Avartar] [nvarchar](max) NULL,
  [Reported] [bit] NULL,
  CONSTRAINT [PK_Student] PRIMARY KEY CLUSTERED ([User_ID])
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[Student]
  ADD CONSTRAINT [FK_Student_User] FOREIGN KEY ([User_ID]) REFERENCES [dbo].[User] ([User_ID])
GO