import operator

class Viterbi:

    #def __init__(self):
        #print 'Running Viterbi algorithm...'

    #returns list of observations with tags
    def tagger(self, obs, tags, trans_p, emit_p): #TODO replace with updated method

        v=[{}]

        #Set first tag (SOS) to probability of 1
        for i in tags:
            if i == 'SOS':
                v[0][i] = 1
            else:
                v[0][i] = 0

        # Run Viterbi when t > 0
        for t in range(1, len(obs)):
            v.append({})
            for y in tags:
                (prob, tag) = max(((v[t-1][y0]+.1) * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in tags) # TODO: Work out why the first term can equal zero and needs the .0001 added to prevent this
                v[t][y] = prob

        #create list of sequence of tags with highest probability for each word
        opt=[]
        for j in v:
            for x,y in j.items():
                if j[x]==max(j.values()):
                    opt.append(x)

        #return original observations with generated tags
        if len(obs) == len(opt):
            return zip(obs, opt)
        else:
            raise NameError('opt (%s) does not match obs (%s) count' % (len(opt), len(obs)))

    def tagger_updated(self, obs, tags, trans_p, emit_p):

        v = [{}]
        opt = []

        #Set first tag (SOS) to probability of 1 and others to 0
        for i in tags:
            if i == 'SOS':
                v[0][i] = 1
            else:
                v[0][i] = 0
        opt.append(max(v[0], key=v[0].get))

        last_complete = 0 #progress percentage tracker

        # Run Viterbi when t > 0
        for t in range(1, len(obs)):
            v.append({})
            for y in tags:
                (prob, tag) = max(((v[t-1][y0]+.1) * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in tags) # TODO: Work out why the first term can equal zero and needs the .0001 added to prevent this
                v[t][y] = prob
            opt.append(max(v[t], key=v[t].get))

            # Print progress
            complete = int(t / float(len(obs))*100)
            if complete > last_complete:
                print '%d%% complete' % complete
                last_complete = complete

        #return original observations with generated tags
        if len(obs) == len(opt):
            return zip(obs, opt)
        else:
            raise NameError('opt (%s) does not match obs (%s) count' % (len(opt), len(obs)))
