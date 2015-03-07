'''
*  This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License.
*
*
*  To view a copy of this license, visit
*
*  English version: http://creativecommons.org/licenses/by-nc-sa/4.0/
*  German version:  http://creativecommons.org/licenses/by-nc-sa/4.0/deed.de
*
*  or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
'''


import xbmc
import xbmcgui
import xbmcaddon


addon = xbmcaddon.Addon("service.idle.actions")
addon_name = addon.getAddonInfo('name')


class IdleActions():
    OnePerStartup = False
    OneAfterTimeout = False

    def __init__(self):
        M = self.Monitor()
        A = self.Actions()
        del M
        del A


    class Actions(xbmcgui.Window):
        def __init__(self):
            idleTime = 0
            isIdle = False
        
            while (not xbmc.abortRequested):
                timeout = int(addon.getSetting('on__idle_time_min')) * 60

                # check for user activity and reset timer
                if xbmc.getGlobalIdleTime() <= 5:  # returns the elapsed idle time in seconds as an integer
                    idleTime = 0                
                    IdleActions.OneAfterTimeout = False

                    if isIdle:
                        # reset random/repeat for onidle
                        if addon.getSetting('on__action') == 'PlayMedia':
                            if addon.getSetting('on__random_playmedia') == 'true':
                                xbmc.executebuiltin('PlayerControl(RandomOff)')
                            if addon.getSetting('on__repeatall_playmedia') == 'true':
                                xbmc.executebuiltin('PlayerControl(RepeatOff)')

                        if addon.getSetting('after__after_idle_action_enabled') == 'true':
                            self.afterIdle()
                        isIdle = False

                if idleTime > timeout:
                    if addon.getSetting('on__service_enabled') == 'true':
                        if not xbmc.Player().isPlaying():
                            isIdle = True

                            actiontype = addon.getSetting('on__action_type')

                            if actiontype == 'one per startup':
                                if not IdleActions.OnePerStartup:
                                    IdleActions.OnePerStartup = True
                                    self.onIdle()

                            if actiontype == 'one after timeout':
                                if not IdleActions.OneAfterTimeout:
                                    IdleActions.OneAfterTimeout = True
                                    self.onIdle()                            

                            if actiontype == 'repeat with timeout':
                                idleTime = 0
                                self.onIdle()

                            if actiontype == 'one per second after timeout':
                                self.onIdle()  


                # reset idleTime if something is played by the user
                if xbmc.Player().isPlaying():
                    idleTime = 0
                else:
                    idleTime = idleTime + 1

                xbmc.sleep(1000)



        # onIdle methods
        def onIdle(self):
            action = addon.getSetting('on__action')
            
            if (action == 'Minimize') or (action == 'Quit') or (action == 'Powerdown') or (action == 'Hibernate') or (action == 'Suspend'):
                xbmc.executebuiltin(action + '()')

            if (action == 'RunScript') or (action == 'RunAppleScript'):
                xbmc.executebuiltin(action + '(' + addon.getSetting('on__file_scripts') + ', ' + addon.getSetting('on__optional_parameter') + ')')

            if (action == 'System.Exec') or (action == 'System.ExecWait'):
                if addon.getSetting('on__execute_file_cmd') == 'File':
                    xbmc.executebuiltin(action + '(' + addon.getSetting('on__file_execs') + ', ' + addon.getSetting('on__optional_parameter') + ')')
                if addon.getSetting('on__execute_file_cmd') == 'CMD':
                    xbmc.executebuiltin(action + '(' + addon.getSetting('on__cmd') + ')')

            if action == 'PlayMedia':
                if addon.getSetting('on__random_playmedia') == 'true':
                    xbmc.executebuiltin('PlayerControl(RandomOn)')
                if addon.getSetting('on__repeatall_playmedia') == 'true':
                    xbmc.executebuiltin('PlayerControl(RepeatAll)')
            
                windowtype = addon.getSetting('on__windowtype')
                if windowtype == 'Fullscreen':
                    windowtypeint = 0
                if windowtype == 'Preview':
                    windowtypeint = 1

                if addon.getSetting('on__type_playmedia') == 'Playlist':
                    if addon.getSetting('on__isdir') == 'true':
                        xbmc.executebuiltin(action + '(' + addon.getSetting('on__folder_playmedia') + ', ' + str(windowtypeint) + ')')
                    else:
                        xbmc.executebuiltin(action + '(' + addon.getSetting('on__file_playmedia') + ', ' + str(windowtypeint) + ', ' + addon.getSetting('on__offset') + ')')

                if addon.getSetting('on__type_playmedia') == 'Audio/Video-File':
                    if addon.getSetting('on__isdir') == 'true':
                        xbmc.executebuiltin(action + '(' + addon.getSetting('on__folder_playmedia') + ', ' + str(windowtypeint) + ')')
                    else:
                        xbmc.executebuiltin(action + '(' + addon.getSetting('on__file_playmedia') + ', ' + str(windowtypeint) + ')')

                if (addon.getSetting('on__type_playmedia') == 'URL'):
                    xbmc.executebuiltin(action + '(' + addon.getSetting('on__url_playmedia') + ', ' + str(windowtypeint) + ')')            

            if action == 'SlideShow':
                if addon.getSetting('on__slideshow_recursive'):
                    xbmc.executebuiltin(action + '(' + addon.getSetting('on__folder') + ', ' + 'recursive' + ', ' + addon.getSetting('on__slideshow_randomtype') + ')')
                else:
                    xbmc.executebuiltin(action + '(' + addon.getSetting('on__folder') + ', ' + addon.getSetting('on__slideshow_randomtype') + ')')

            if action == 'RecursiveSlideShow':
                xbmc.executebuiltin(action + '(' + addon.getSetting('on__folder') + ')')

            if action == 'UpdateLibrary':
                if addon.getSetting('on__update_clean_library') == 'music':
                    xbmc.executebuiltin(action + '(music)')
                if addon.getSetting('on__update_clean_library') == 'video':
                    xbmc.executebuiltin(action + '(video' + ', ' + addon.getSetting('on__opt_fol__upd_vid_lib') + ')')

            if action == 'CleanLibrary':
                xbmc.executebuiltin(action + '(' + addon.getSetting('on__update_clean_library') + ')')

            if action == 'PlayDVD':
                dvdstate = xbmc.getDVDState()
                if dvdstate == 1:                
                    xbmc.executebuiltin('Notification(%s, Error: Drive not ready)' %(addon_name) )
                elif dvdstate == 16:
                    xbmc.executebuiltin('Notification(%s, Error: Tray open)' %(addon_name) )
                elif dvdstate == 64:
                    xbmc.executebuiltin('Notification(%s, Error: No media)' %(addon_name) )
                else:
                    xbmc.executebuiltin(action + '()')
        
            if action == 'ActivateScreensaver':
                ver = xbmc.getInfoLabel('System.BuildVersion')
                verint = int(ver.replace(ver[ver.find('.'):], ''))
                if verint > 12:
                    xbmc.executebuiltin(action + '()')


            xbmc.sleep(1000)
            if xbmc.Player().isPlaying():
                while (not xbmc.abortRequested):            
                    timeout = int(addon.getSetting('on__idle_time_min'))
                    idleTime = xbmc.getGlobalIdleTime()
                    if idleTime < timeout:
                        xbmc.executebuiltin('PlayerControl(Stop)')
                        break

                xbmc.sleep(1000)


        # afterIdle methods
        def afterIdle(self):
            action = addon.getSetting('after__action')
            
            if (action == 'Minimize') or (action == 'Quit') or (action == 'Powerdown') or (action == 'Hibernate') or (action == 'Suspend'):
                xbmc.executebuiltin(action + '()')

            if (action == 'RunScript') or (action == 'RunAppleScript'):
                xbmc.executebuiltin(action + '(' + addon.getSetting('after__file_scripts') + ', ' + addon.getSetting('after__optional_parameter') + ')')

            if (action == 'System.Exec') or (action == 'System.ExecWait'):
                if addon.getSetting('after__execute_file_cmd') == 'File':
                    xbmc.executebuiltin(action + '(' + addon.getSetting('after__file_execs') + ', ' + addon.getSetting('after__optional_parameter') + ')')
                if addon.getSetting('after__execute_file_cmd') == 'CMD':
                    xbmc.executebuiltin(action + '(' + addon.getSetting('after__cmd') + ')')

            if action == 'PlayMedia':
                if addon.getSetting('after__random_playmedia') == 'true':
                    xbmc.executebuiltin('PlayerControl(RandomOn)')
                if addon.getSetting('after__repeatall_playmedia') == 'true':
                    xbmc.executebuiltin('PlayerControl(RepeatAll)')
                
                windowtype = addon.getSetting('after__windowtype')
                if windowtype == 'Fullscreen':
                    windowtypeint = 0
                if windowtype == 'Preview':
                    windowtypeint = 1

                if addon.getSetting('after__type_playmedia') == 'Playlist':
                    if addon.getSetting('after__isdir') == 'true':
                        xbmc.executebuiltin(action + '(' + addon.getSetting('after__folder_playmedia') + ', ' + str(windowtypeint) + ')')
                    else:
                        xbmc.executebuiltin(action + '(' + addon.getSetting('after__file_playmedia') + ', ' + str(windowtypeint) + ', ' + addon.getSetting('after__offset') + ')')

                if addon.getSetting('after__type_playmedia') == 'Audio/Video-File':
                    if addon.getSetting('after__isdir') == 'true':
                        xbmc.executebuiltin(action + '(' + addon.getSetting('after__folder_playmedia') + ', ' + str(windowtypeint) + ')')
                    else:
                        xbmc.executebuiltin(action + '(' + addon.getSetting('after__file_playmedia') + ', ' + str(windowtypeint) + ')')

                if (addon.getSetting('after__type_playmedia') == 'URL'):
                    xbmc.executebuiltin(action + '(' + addon.getSetting('after__url_playmedia') + ', ' + str(windowtypeint) + ')')            

            if action == 'SlideShow':
                if addon.getSetting('after__slideshow_recursive'):
                    xbmc.executebuiltin(action + '(' + addon.getSetting('after__folder') + ', ' + 'recursive' + ', ' + addon.getSetting('after__slideshow_randomtype') + ')')
                else:
                    xbmc.executebuiltin(action + '(' + addon.getSetting('after__folder') + ', ' + addon.getSetting('after__slideshow_randomtype') + ')')

            if action == 'RecursiveSlideShow':
                xbmc.executebuiltin(action + '(' + addon.getSetting('after__folder') + ')')

            if action == 'UpdateLibrary':
                if addon.getSetting('after__update_clean_library') == 'music':
                    xbmc.executebuiltin(action + '(music)')
                if addon.getSetting('after__update_clean_library') == 'video':
                    xbmc.executebuiltin(action + '(video' + ', ' + addon.getSetting('after__opt_fol__upd_vid_lib') + ')')

            if action == 'CleanLibrary':
                xbmc.executebuiltin(action + '(' + addon.getSetting('after__update_clean_library') + ')')

            if action == 'PlayDVD':
                dvdstate = xbmc.getDVDState()
                if dvdstate == 1:                
                    xbmc.executebuiltin('Notification(%s, Error: Drive not ready)' %(addon_name) )
                elif dvdstate == 16:
                    xbmc.executebuiltin('Notification(%s, Error: Tray open)' %(addon_name) )
                elif dvdstate == 64:
                    xbmc.executebuiltin('Notification(%s, Error: No media)' %(addon_name) )
                else:
                    xbmc.executebuiltin(action + '()')

            if action == 'ActivateScreensaver':
                ver = xbmc.getInfoLabel('System.BuildVersion')
                verint = int(ver.replace(ver[ver.find('.'):], ''))
                if verint > 12:
                    xbmc.executebuiltin(action + '()')


            

    class Monitor(xbmc.Monitor):
        def onSettingsChanged(self):    
            if ((addon.getSetting('on__action_type') == 'one per startup') or (addon.getSetting('on__action_type') == 'one after timeout')) and (addon.getSetting('on__service_enabled') == 'true'):
                dlg = xbmcgui.Dialog()
                if dlg.yesno('%s' %(addon_name) , 'Activate Action?'):
                    IdleActions.OnePerStartup = False
                    IdleActions.OneAfterTimeout = False
                else:
                    IdleActions.OnePerStartup = True
                    IdleActions.OneAfterTimeout = True
        



if __name__ == '__main__':
    IA = IdleActions()
    del IA
