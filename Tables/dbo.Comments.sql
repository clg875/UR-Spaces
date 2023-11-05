CREATE TABLE [dbo].[Comments] (
  [Comment_ID] [int] IDENTITY,
  [Post_ID] [int] NOT NULL,
  [User_ID] [int] NOT NULL,
  [Likes] [int] NULL,
  [PIn] [bit] NULL,
  [Reported] [bit] NULL,
  [Com_Contents] [nvarchar](max) NOT NULL,
  [Com_Date] [datetime] NOT NULL,
  CONSTRAINT [PK_Comments] PRIMARY KEY CLUSTERED ([Comment_ID])
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[Comments]
  ADD CONSTRAINT [FK_Comments_Posts] FOREIGN KEY ([Post_ID]) REFERENCES [dbo].[Posts] ([Post_ID])
GO

ALTER TABLE [dbo].[Comments]
  ADD CONSTRAINT [FK_Comments_Student] FOREIGN KEY ([User_ID]) REFERENCES [dbo].[Student] ([User_ID])
GO