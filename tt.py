import wx
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def load_words(self, word_list):
        for word in word_list:
            self.add_word(word)

    def add_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def auto_correct(self, word):
        node = self.root
        if word[0] not in node.children:
            return [word]
        for i, char in enumerate(word):
            if char not in node.children:
                return self.auto_fill(word[:i], node)
            node = node.children[char]
        return [word]

    def auto_fill(self, prefix, node=None):
        if node is None:
            node = self.root
            for char in prefix:
                if char not in node.children:
                    return []
                node = node.children[char]
        words = []
        if node.is_word:
            words.append(prefix)
        for char, child in node.children.items():
            words.extend(self.auto_fill(prefix + char, child))
        return words

    def spell_check(self, sentence):
        words = sentence.split()
        misspelled = []
        for word in words:
            if not self.check_word(word):
                misspelled.append(word)
        return misspelled

    def check_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Trie')
        self.SetSize((500,300))
        panel = wx.Panel(self)
        self.Center()
        panel.SetBackgroundColour(wx.Colour(17, 236, 247))
        label = wx.StaticText(panel, label='Enter a sentence:')
        self.textbox = wx.TextCtrl(panel)
        button1 = wx.Button(panel, label='Auto Correct')
        button2 = wx.Button(panel, label='Auto Suggest')
        button3 = wx.Button(panel, label='Spell Check')
        self.result_label = wx.StaticText(panel, label='')
    
        self.trie = Trie()
        with open('Hello.txt') as f:
            word_list = f.read().split()
        print("Words in the file are: ")
        print(*word_list)
        self.trie.load_words(word_list)

        button1.Bind(wx.EVT_BUTTON, self.ac)
        button2.Bind(wx.EVT_BUTTON, self.a1s)
        button3.Bind(wx.EVT_BUTTON, self.sc)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.ALL, 5)
        sizer.Add(self.textbox, 0, wx.ALL, 5)
        sizer.Add(button1, 0, wx.ALL, 5)
        sizer.Add(button2, 0, wx.ALL, 5)
        sizer.Add(button3, 0, wx.ALL, 5)
        sizer.Add(self.result_label, 0, wx.ALL, 5)
        panel.SetSizer(sizer)

        self.Show()

    def ac(self, event):
        word = self.textbox.GetValue()
        corrected_words = self.trie.auto_correct(word)
        print(corrected_words)
        cv=[]
        for i in word:
            cv.append(i)
        ll={}
        for i in corrected_words :
            if len(i)==len(word):
                print(i)
            ll[i]=0
        for i in ll:
            for j in cv:
                if j in i:
                    ll[i]+=1
        print("Mostly resembles the word: ",end=" ")
        print(max(ll,key=ll.get))
    
        self.result_label.SetLabel("Corrected word: " + max(ll,key=ll.get))
        

    def a1s(self, event):
        prefix = self.textbox.GetValue()
        words = self.trie.auto_fill(prefix)
        self.result_label.SetLabel("Suggested words: " + ", ".join(words))

    def sc(self, event):
        sentence = self.textbox.GetValue()
        misspelled_words = self.trie.spell_check(sentence)
        if not misspelled_words:
            self.result_label.SetLabel("No misspelled words found.")
        else:
            self.result_label.SetLabel("Misspelled words: " + ", ".join(misspelled_words))


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
