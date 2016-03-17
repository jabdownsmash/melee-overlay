
    # def listener2 (self,state):
    #     for fi in self.fis:
    #         fi.alpha -= .002
    #         if fi.alpha < 0:
    #             fi.alpha = 0
    #         fi.update()

    # def listener (self,state):
    #     # print(str(state.players[0].action_state) + " " + str(state.players[0].fastfall_velocity) + " " + str(state.players[0].vertical_velocity))
    #     if state.players[0].vertical_velocity < 0 and state.players[0].vertical_velocity + state.players[0].fastfall_velocity > 0:
    #         if self.newFI:
    #             self.newFI = False
    #             self.fi = FrameIndicator()

    #             self.fi.setParent(self.cont)
    #             self.fi.center = 0
    #             self.fi.resize(80,8)
    #             self.fi.show()

    #             # self.fi.move(100,200)
    #         self.fi.frameCounter += 1
    #         self.fi.setFrame(self.fi.frameCounter)


    #         x,y = self.board.transformPoint(state.players[0].x,-(state.players[0].y + 10))
    #         self.fi.move(x  - self.fi.width()/2,y)
    #     else:
    #         self.newFI = True
    #         try:
    #             self.fis.append(self.fi)
    #         except AttributeError:
    #             pass