CREATE TABLE [dbo].[Likes] (
  [Like_ID] [int] IDENTITY,
  [Post_ID] [int] NOT NULL,
  [User_ID] [int] NOT NULL,
  [Comment_ID] [int] NULL,
  [likes] [int] NOT NULL,
  CONSTRAINT [PK_Likes] PRIMARY KEY CLUSTERED ([Like_ID])
)
ON [PRIMARY]
GO

ALTER TABLE [dbo].[Likes]
  ADD CONSTRAINT [FK_Likes_Comments] FOREIGN KEY ([Comment_ID]) REFERENCES [dbo].[Comments] ([Comment_ID])
GO

ALTER TABLE [dbo].[Likes]
  ADD CONSTRAINT [FK_Likes_Posts] FOREIGN KEY ([Post_ID]) REFERENCES [dbo].[Posts] ([Post_ID])
GO

ALTER TABLE [dbo].[Likes]
  ADD CONSTRAINT [FK_Likes_Student] FOREIGN KEY ([User_ID]) REFERENCES [dbo].[Student] ([User_ID])
GO