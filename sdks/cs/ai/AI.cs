namespace ai
{
    public struct Move
    {
        public int Column;
        public Move(int move)
        {
            Column = move;
        }
    }

    public static class AI
    {
        public static int[] NextMove(GameMessage gameMessage)
        {
            var nextMove = new Move(1);
            return nextMove;
        }

    }
}
