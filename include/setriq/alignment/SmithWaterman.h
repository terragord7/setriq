//
// Created by Benjamin Tenmann on 21/11/2021.
//

#ifndef METRICS_SMITHWATERMAN_H
#define METRICS_SMITHWATERMAN_H

#include "SubstitutionMatrix.h"
#include "utils/LRUCache.h"
#include "utils/typeDefs.h"

class SmithWaterman {
private:
    LRUCache<std::string, double> cache;
    SubstitutionMatrix substitutionMatrix;
    double gapPenalty;

    // scoring matrix creation
    double calculateGapPenalty(const doubleMatrix&, const size_t&, const size_t&, const size_t&) const;
    double fillScoringMatrix(doubleMatrix&, const std::string&, const std::string&);
    double computeBestAlignmentScore(const std::string&, const std::string&);

public:
    SmithWaterman() : cache(), substitutionMatrix(), gapPenalty{0} {};
    SmithWaterman(SubstitutionMatrix, double, size_t);

    double forward(const std::string&, const std::string&);
    double operator() (const std::string& a, const std::string& b) {
        if (this->cache.exists(a + b)) {
            return this->cache.get(a + b);
        }
        double out {this->forward(a, b)};

        this->cache.put(a + b, out);
        return out;
    };

    // special case: identity score
    double identityScore(const std::string&);
};


#endif //METRICS_SMITHWATERMAN_H
