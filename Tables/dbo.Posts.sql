CREATE TABLE [dbo].[Posts] (
  [Post_ID] [int] IDENTITY,
  [User_ID] [int] NOT NULL,
  [Post_name] [nvarchar](50) NOT NULL,
  [Post_sub_name] [nvarchar](50) NOT NULL,
  [Sub_id] [int] NOT NULL,
  [Contents] [nvarchar](max) NOT NULL,
  [Likes] [int] NULL,
  [Locked] [bit] NULL,
  [Reported] [bit] NULL,
  [Pin] [bit] NULL,
  [Post_Date] [datetime] NOT NULL,
  [Comments] [int] NOT NULL,
  CONSTRAINT [PK_Posts] PRIMARY KEY CLUSTERED ([Post_ID])
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[Posts]
  ADD CONSTRAINT [FK_Posts_Student] FOREIGN KEY ([User_ID]) REFERENCES [dbo].[Student] ([User_ID])
GO