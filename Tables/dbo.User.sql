CREATE TABLE [dbo].[User] (
  [User_ID] [int] IDENTITY,
  [User_Name] [varchar](50) NOT NULL,
  [Email_Address] [nvarchar](max) NOT NULL,
  [Password] [varchar](50) NOT NULL,
  [User_Date] [date] NOT NULL,
  CONSTRAINT [PK_User] PRIMARY KEY CLUSTERED ([User_ID])
)
ON [PRIMARY]
TEXTIMAGE_ON [PRIMARY]
GO