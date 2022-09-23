-- CreateTable
CREATE TABLE "Task" (
    "id" TEXT NOT NULL,
    "task" TEXT NOT NULL,
    "done" BOOLEAN NOT NULL DEFAULT false,
    "due" TIMESTAMP(3) NOT NULL DEFAULT (now() + interval '2 days'),
    "user_id" TEXT,

    CONSTRAINT "Task_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "User" (
    "id" TEXT NOT NULL,
    "username" TEXT NOT NULL,
    "password" TEXT NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Token" (
    "access_token" TEXT NOT NULL,
    "token_type" TEXT NOT NULL DEFAULT E'bearer',
    "expiry_date" TIMESTAMP(3) NOT NULL DEFAULT (now() + interval '2 days'),
    "user_id" TEXT NOT NULL,

    CONSTRAINT "Token_pkey" PRIMARY KEY ("access_token")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_username_key" ON "User"("username");

-- AddForeignKey
ALTER TABLE "Task" ADD CONSTRAINT "Task_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Token" ADD CONSTRAINT "Token_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
